"""Phase 2 of the adopt-update-build study: docs/prereg_realism_harmonization.md (OSF 10.17605/OSF.IO/SAJEX).

Three sets of units: H (single eICU-CRD hospitals; hypotension and O2), T (MIMIC-IV, local pool 2008-2016, test
2017-2022; hypotension, O1, O2) and M (rotation units with controlled harmonization errors M0-M3 in what the external
model sees). Balanced options: update and build choose their boosting iterations by 3-fold patient-grouped CV on the
n patients and are refitted on all of them; variants update_tuned, build_tuned, build_lr. Choice by cross-validation,
the closed test and rule v2; hypotheses G1-G4 as registered.

Usage:  python scripts/phase2_realism.py --set H|T|M [--units ...] [--threads 4]
Outputs (aggregates only): <experiments>/hypo/review/phase2_<set>.json and reports/phase2_realism.md
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import logging
import sys
import time
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_analyses as RA  # noqa: E402
import posthoc_own_vs_external as OE  # noqa: E402
import posthoc_r8_hypo as R8  # noqa: E402
import phase1_new_outcomes as P1  # noqa: E402
import own_ext_common as C  # noqa: E402

LOG = logging.getLogger("phase2")
REGISTRATION = "10.17605/OSF.IO/SAJEX"
GRID = [(nl, md) for nl in (7, 15, 31) for md in (20, 100)]
FIXED = (31, 50)
INNER = 3
MAX_IT, PATIENCE = 2000, 50
NB_T = {"hypo": (0.10, 0.20, 0.30), "O1": (0.05, 0.10, 0.20), "O2": (0.30, 0.50, 0.70)}
H_MIN_PATIENTS = 600
SIZES = {"H": (100, 250, 500), "T": (250, 500, 1000, 2000, 4000), "M": (250, 1000, 4000)}
DRAWS = {"H": {100: 5, 250: 5, 500: 5}, "T": {250: 10, 500: 10, 1000: 10, 2000: 5, 4000: 5},
         "M": {250: 2, 1000: 2, 4000: 2}}
LEVELS = ("M0", "M1", "M2", "M3")
ROT = {"hypo": ("inspire", "mimic", "eicu"), "O1": ("mimic", "eicu"), "O2": ("inspire", "mimic", "eicu")}
O_SOURCES = {"O1": {"mimic": ("eicu",), "eicu": ("mimic",)},
             "O2": {"inspire": ("mimic", "eicu"), "mimic": ("inspire", "eicu"), "eicu": ("inspire", "mimic")}}


# =========================================================================== harmonization errors (tested)
def perturb(lm, level: str):
    """A copy of the landmarks with the registered harmonization errors of `level` (cumulative)."""
    if level == "M0":
        return lm
    k = LEVELS.index(level)
    num = {name: np.array(v, dtype=np.float64, copy=True) for name, v in lm.ft.num.items()}
    cat = {name: np.array(v, dtype=object, copy=True) for name, v in lm.ft.cat.items()}
    if k >= 1:
        for name, f in (("lactate_last", 9.01), ("creatinine_last", 88.4), ("hb_last", 10.0)):
            if name in num:
                num[name] = num[name] * f
        if "temp_last" in num:
            num["temp_last"] = num["temp_last"] * 1.8 + 32.0
    if k >= 2:
        if "map_min_6h" in num and "map_mean_6h" in num:
            num["map_min_6h"] = num["map_mean_6h"].copy()
        for name in ("vent_on", "sedation_on", "sedation_24h"):
            if name in num:
                num[name] = np.full(len(lm.ft), np.nan)
    if k >= 3:
        if "surgical_group" in cat:
            cat["surgical_group"] = np.array(["unmapped"] * len(lm.ft), dtype=object)
        if "emergency" in num:
            num["emergency"] = np.full(len(lm.ft), np.nan)
    ft = dataclasses.replace(lm.ft, num=num, cat=cat)
    return dataclasses.replace(lm, ft=ft)


# =========================================================================== balanced LightGBM (tested)
def _train(X, y, Xv, yv, cat_idx, params, init=None, init_v=None, rounds=MAX_IT, stop=True):
    import lightgbm as lgb
    dtr = lgb.Dataset(X, y, init_score=init, categorical_feature=cat_idx, free_raw_data=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if not stop:
            return lgb.train(params, dtr, rounds)
        dva = lgb.Dataset(Xv, yv, init_score=init_v, reference=dtr, categorical_feature=cat_idx)
        return lgb.train(params, dtr, rounds, valid_sets=[dva], callbacks=[lgb.early_stopping(PATIENCE, verbose=False)])


def _params(seed, threads, leaves, min_data):
    return {"objective": "binary", "learning_rate": 0.05, "num_leaves": leaves, "min_data_in_leaf": min_data,
            "bagging_fraction": 0.8, "bagging_freq": 1, "feature_fraction": 0.8, "deterministic": True,
            "force_col_wise": True, "num_threads": threads, "seed": seed, "verbose": -1}


def cv_iterations(X, y, subj, cat_idx, seed, threads, leaves, min_data, init=None) -> tuple[int, float]:
    """Mean best iteration over 3 patient-grouped folds and the summed held-out log-loss at those iterations."""
    from sklearn.model_selection import GroupKFold
    its, loss = [], 0.0
    for a, b in GroupKFold(INNER).split(X, groups=subj):
        if y[a].min() == y[a].max() or y[b].min() == y[b].max():
            continue
        m = _train(X[a], y[a], X[b], y[b], cat_idx, _params(seed, threads, leaves, min_data),
                   None if init is None else init[a], None if init is None else init[b])
        it = int(m.best_iteration or m.current_iteration())
        its.append(it)
        raw = m.predict(X[b], num_iteration=it, raw_score=True) + (0.0 if init is None else init[b])
        loss += float(RA.PP.ll_rows(RA.sigmoid(raw), y[b]).sum())
    return (int(round(np.mean(its))) if its else 50), loss


def lgbm_balanced(X, y, subj, X_te, cat_idx, seed, threads, grid=(FIXED,), init=None, init_te=None):
    """Iterations (and, with a grid, leaves × min_data) by inner CV; refit on all n; predictions on X_te."""
    y = np.asarray(y, dtype=np.float64)
    base_te = 0.0 if init_te is None else init_te
    if y.min() == y.max():
        return RA.sigmoid(base_te + (RA.logit(np.full(X_te.shape[0], y.mean())) if init_te is None else 0.0)), {}
    scored = [(g, *cv_iterations(X, y, subj, cat_idx, seed, threads, *g, init=init)) for g in grid]
    g, it, _ = min(scored, key=lambda t: t[2])
    m = _train(X, y, None, None, cat_idx, _params(seed, threads, *g), init=init, rounds=max(it, 1), stop=False)
    return RA.sigmoid(base_te + m.predict(X_te, raw_score=True)), {"leaves": g[0], "min_data": g[1], "iterations": it}


# =========================================================================== one sample
def fit_options(Xraw, cat_idx, plg, y, subj, fit, te, seed, threads, tuned=True) -> tuple[dict, dict]:
    lp = RA.logit(plg)
    P, info = {}, {}
    P["keep"] = plg[te]
    P["intercept"] = RA.recal("intercept", plg[fit], y[fit], plg[te])
    P["adopt"] = RA.recal("logistic", plg[fit], y[fit], plg[te])
    P["update"], info["update"] = lgbm_balanced(Xraw[fit], y[fit], subj[fit], Xraw[te], cat_idx, seed, threads,
                                                init=lp[fit], init_te=lp[te])
    P["build"], info["build"] = lgbm_balanced(Xraw[fit], y[fit], subj[fit], Xraw[te], cat_idx, seed, threads)
    if tuned:
        P["update_tuned"], info["update_tuned"] = lgbm_balanced(Xraw[fit], y[fit], subj[fit], Xraw[te], cat_idx,
                                                                seed, threads, GRID, lp[fit], lp[te])
        P["build_tuned"], info["build_tuned"] = lgbm_balanced(Xraw[fit], y[fit], subj[fit], Xraw[te], cat_idx, seed,
                                                              threads, GRID)
        P["build_lr"], info["build_lr"] = R8.own_lr(Xraw, y, subj, fit, te, cat_idx, seed)
    return P, info


def cv_choice(Xraw, cat_idx, plg, y, subj, fit, seed, threads) -> str:
    from sklearn.model_selection import GroupKFold
    L = {a: 0.0 for a in C.OPTIONS}
    for i, (a, b) in enumerate(GroupKFold(INNER).split(fit, groups=subj[fit])):
        P, _ = fit_options(Xraw, cat_idx, plg, y, subj, fit[a], fit[b], seed + 31 * (i + 1), threads, tuned=False)
        for k, name in (("adopt", "adopt"), ("update", "update"), ("own", "build")):
            L[k] += float(RA.PP.ll_rows(P[name], y[fit[b]]).sum())
    return min(C.OPTIONS, key=lambda k: L[k])


def closed_choice(Xraw, cat_idx, plg, y, subj, fit, seed, threads) -> str:
    pats = np.unique(subj[fit])
    rng = np.random.default_rng(seed + 11)
    fp = np.isin(subj[fit], rng.permutation(pats)[:int(round(2 / 3 * pats.size))])
    f, v = fit[fp], fit[~fp]
    P, _ = fit_options(Xraw, cat_idx, plg, y, subj, f, v, seed + 13, threads, tuned=False)
    L = {"keep": P["keep"], "intercept": P["intercept"], "logistic": P["adopt"], "update": P["update"],
         "own": P["build"]}
    return C.closed_choice({k: RA.PP.ll_rows(p, y[v]) for k, p in L.items()}, subj[v])


def sample(Xraw, cat_idx, plg, y, subj, fit, te, n, seed, thresholds, threads) -> dict:
    P, info = fit_options(Xraw, cat_idx, plg, y, subj, fit, te, seed, threads)
    L = {k: OE.ll(p, y[te]) for k, p in P.items()}
    L["logistic"] = L["adopt"]
    L["own"] = L["build"]                                   # the registered "build" under review-8 names
    best_ext = min(("adopt", "update", "update_tuned"), key=lambda k: L[k])
    best_own = min(("build", "build_tuned", "build_lr"), key=lambda k: L[k])
    dg = OE.diagnostics(plg[fit], y[fit], seed + 3)
    rec = {"ll": L, "auc": {k: OE.auc(P[k], y[te]) for k in ("adopt", "update", "build", "keep")},
           "best_ext": best_ext, "best_own": best_own, "own_beats_ext": bool(L[best_own] < L[best_ext]),
           "diag": dg, "flag": C.relation_shift(dg),
           "cv_choice": cv_choice(Xraw, cat_idx, plg, y, subj, fit, seed, threads),
           "closed_choice": closed_choice(Xraw, cat_idx, plg, y, subj, fit, seed, threads),
           "rule_v2_choice": C.rule_v2_choice(dg, n),
           "nb": {f"t{t:.2f}": {k: C.net_benefit(P[k], y[te], t) for k in ("adopt", "update", "build")}
                  for t in thresholds},
           "events": {"landmarks": int(y[fit].sum()), "patients": int(np.unique(subj[fit][y[fit] == 1]).size)},
           "info": info}
    return rec


# =========================================================================== units
class Unit2:
    def __init__(self, name, set_, outcome, lm, plg, seed, ci, fold=None, fit_pool=None, test=None):
        self.name, self.set, self.outcome, self.lm, self.plg = name, set_, outcome, lm, plg
        self.seed, self.ci, self.fold, self.fit_pool, self.test = seed, ci, fold, fit_pool, test
        self.y = lm.y.astype(np.float64)
        self.subj = np.asarray(lm.ft.subjects).astype(str)

    def splits(self):
        """(label, training positions, test positions): 5 patient folds, or the fixed temporal split."""
        if self.fold is not None:
            for f in sorted(set(self.fold.tolist())):
                yield f, np.where(self.fold != f)[0], np.where(self.fold == f)[0]
        else:
            yield 0, self.fit_pool, self.test

    def draw(self, f, tr, n, r):
        s = self.subj[tr]
        uniq = np.unique(s)
        rng = np.random.default_rng([int(self.seed), 9, self.ci, int(f), int(n), int(r)])
        pick = rng.choice(uniq, size=min(n, uniq.size), replace=False)
        return tr[np.isin(s, pick)]


def run_unit(u: Unit2, cache: Path, threads: int) -> dict:
    Xraw, cat_idx = RA.raw_matrix(u.lm, RA.cat_levels(u.lm))
    splits = list(u.splits())
    min_pool = min(np.unique(u.subj[tr]).size for _, tr, _ in splits)
    sizes = [n for n in SIZES[u.set] if n < min_pool]
    thresholds = NB_T[u.outcome]
    samples = []
    for n in sizes:
        for r in range(DRAWS[u.set][n]):
            for f, tr, te in splits:
                path = cache / f"{u.name}_n{n}_r{r}_f{f}.json"
                if path.exists():
                    samples.append(json.loads(path.read_text(encoding="utf-8")))
                    continue
                t0 = time.perf_counter()
                fit = u.draw(f, tr, n, r)
                rec = {"n": n, "r": r, "f": int(f), "test_rows": int(te.size)}
                rec.update(sample(Xraw, cat_idx, u.plg, u.y, u.subj, fit, te, n,
                                  u.seed + 100 * int(f) + 17 * r + n, thresholds, threads))
                rec["seconds"] = time.perf_counter() - t0
                path.write_text(json.dumps(rec, default=float), encoding="utf-8")
                samples.append(rec)
                LOG.info("phase2 %s n=%d r=%d f%d: cv→%s, closed→%s, best ext %s / own %s (%.0f s)", u.name, n, r, f,
                         rec["cv_choice"], rec["closed_choice"], rec["best_ext"], rec["best_own"], rec["seconds"])
    return summarise_unit(u, samples, sizes, thresholds)


def summarise_unit(u, samples, sizes, thresholds) -> dict:
    out = {"unit": u.name, "set": u.set, "outcome": u.outcome, "sizes": sizes, "by_n": {},
           "destination": {"landmarks": int(u.y.size), "patients": int(np.unique(u.subj).size),
                           "prevalence": float(u.y.mean())}, "registration": REGISTRATION}
    for n in sizes:
        S = [s for s in samples if s["n"] == n]
        if not S:
            continue
        best = [min(C.OPTIONS, key=lambda a: s["ll"][a]) for s in S]
        o = {"samples": len(S), "logloss_mean": {k: float(np.mean([s["ll"][k] for s in S])) for k in S[0]["ll"]}}
        for a, b in (("build", "update"), ("build", "adopt"), ("update", "adopt"), ("build_tuned", "update_tuned"),
                     ("build_lr", "adopt")):
            d = np.array([s["ll"][a] - s["ll"][b] for s in S])
            o[f"{a}_vs_{b}"] = {"mean": float(d.mean()), "share_wins": float((d < 0).mean())}
        d = np.array([s["ll"][s["best_own"]] - s["ll"][s["best_ext"]] for s in S])
        o["best_own_vs_best_ext"] = {"mean": float(d.mean()), "share_wins": float((d < 0).mean())}
        o["policies"] = {}
        for name, key in (("cv", "cv_choice"), ("closed_test", "closed_choice"), ("rule_v2", "rule_v2_choice")):
            ch = [s[key] for s in S]
            reg = [s["ll"][c] - s["ll"][b] for s, c, b in zip(S, ch, best)]
            o["policies"][name] = {"regret_mean": float(np.mean(reg)), "regret_p90": float(np.percentile(reg, 90)),
                                   "correct_share": float(np.mean([c == b for c, b in zip(ch, best)])),
                                   "chosen_share": {c: float(np.mean([x == c for x in ch])) for c in sorted(set(ch))}}
        o["flag_share"] = float(np.mean([s["flag"] for s in S]))
        o["net_benefit"] = {}
        for t in thresholds:
            k = f"t{t:.2f}"
            for a in ("update", "build"):
                v = np.array([100 * (s["nb"][k][a] - s["nb"][k]["adopt"]) for s in S])
                o["net_benefit"][f"{k}|{a}_vs_adopt_per_100_landmarks"] = float(v.mean())
        o["events_mean"] = {k: float(np.mean([s["events"][k] for s in S])) for k in S[0]["events"]}
        out["by_n"][str(n)] = o
    be = {}
    for key in ("build_vs_update", "build_vs_adopt", "update_vs_adopt", "build_tuned_vs_update_tuned",
                "best_own_vs_best_ext"):
        hit = [n for n in sizes if str(n) in out["by_n"] and out["by_n"][str(n)][key]["share_wins"] >= 0.8]
        be[key] = hit[0] if hit else None
    out["breakeven_80pct"] = be
    out["pairs"] = [[bool(s["flag"]), bool(s["own_beats_ext"])] for s in samples]     # for G2 (no patient data)
    return out


# =========================================================================== hypotheses (tested)
def risk_difference_ci(pairs_by_unit: dict, n_boot: int = 2000, seed: int = 0) -> dict:
    """G2: P(own beats ext | flag) − P(own beats ext | no flag), pooled, with a unit-clustered bootstrap CI; and
    sensitivity, specificity, PPV, NPV of the flag for 'own beats ext'."""
    units = sorted(pairs_by_unit)

    def stats(sel):
        a = np.array([p for u in sel for p in pairs_by_unit[u]], dtype=bool).reshape(-1, 2)
        f, w = a[:, 0], a[:, 1]
        rd = (w[f].mean() if f.any() else np.nan) - (w[~f].mean() if (~f).any() else np.nan)
        sens = (f & w).sum() / max(w.sum(), 1)
        spec = (~f & ~w).sum() / max((~w).sum(), 1)
        ppv = (f & w).sum() / max(f.sum(), 1)
        npv = (~f & ~w).sum() / max((~f).sum(), 1)
        return {"rd": rd, "sens": sens, "spec": spec, "ppv": ppv, "npv": npv, "flagged": int(f.sum()),
                "own_wins": int(w.sum()), "samples": int(f.size)}

    est = stats(units)
    rng = np.random.default_rng(seed)
    B = {k: [] for k in ("rd", "sens", "spec", "ppv", "npv")}
    for _ in range(n_boot):
        s = stats(list(rng.choice(units, size=len(units), replace=True)))
        for k in B:
            if np.isfinite(s[k]):
                B[k].append(s[k])
    ci = {k: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if v else [None, None] for k, v in B.items()}
    holds = bool(ci["rd"][0] is not None and ci["rd"][0] > 0)
    return {"estimate": {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in est.items()},
            "ci95": ci, "holds": holds}


def mantel_trend(strata: list[list[tuple[int, int]]], scores=(0, 1, 2, 3)) -> dict:
    """Stratified linear trend test (Mantel 1963 extension). Each stratum: a list of (successes, trials) per level."""
    from scipy.stats import norm
    num, var = 0.0, 0.0
    for st in strata:
        s = np.array(scores[:len(st)], dtype=float)
        x = np.array([a for a, _ in st], dtype=float)
        m = np.array([b for _, b in st], dtype=float)
        N, X = m.sum(), x.sum()
        if N < 2 or X == 0 or X == N:
            continue
        e = m * X / N
        num += float((s * (x - e)).sum())
        var += float(X * (N - X) / (N * N * (N - 1)) * (N * (m * s * s).sum() - (m * s).sum() ** 2))
    z = num / np.sqrt(var) if var > 0 else 0.0
    return {"z": float(z), "p_one_sided": float(1 - norm.cdf(z))}


def hypotheses(res: dict) -> dict:
    units = {k: v for k, v in res.items() if isinstance(v, dict) and "set" in v and "dropped" not in v}
    out = {}
    g1 = [k for k, u in units.items() if u["set"] in ("H", "T")]
    exc = [k for k in g1 if units[k]["breakeven_80pct"]["build_vs_update"] is not None]
    out["G1"] = {"units": len(g1), "exceptions": exc,
                 "verdict": "not evaluable" if not g1 else ("holds" if not exc else
                                                            ("partial failure" if len(exc) == 1 else "failure"))}
    pairs = {k: u["pairs"] for k, u in units.items()}
    out["G2"] = risk_difference_ci(pairs) if pairs else {"verdict": "not evaluable"}
    if pairs:
        out["G2"]["verdict"] = "holds" if out["G2"]["holds"] else "fails"
    m = {k: u for k, u in units.items() if u["set"] == "M"}
    if m:
        base = {}
        for k, u in m.items():
            b, lev = k.rsplit("_", 1)
            base.setdefault(b, {})[lev] = u
        strata = []
        for b, levs in base.items():
            if all(L in levs for L in LEVELS):
                strata.append([(sum(p[1] for p in levs[L]["pairs"]), len(levs[L]["pairs"])) for L in LEVELS])
        tr = mantel_trend(strata)
        hits = [b for b, levs in base.items() if "M3" in levs and "4000" in levs["M3"]["by_n"]
                and levs["M3"]["by_n"]["4000"]["build_vs_update"]["share_wins"] >= 0.8]
        reach = [b for b, levs in base.items() if "M3" in levs and "4000" in levs["M3"]["by_n"]]
        share = {L: float(np.mean([p[1] for levs in base.values() if L in levs for p in levs[L]["pairs"]]))
                 for L in LEVELS}
        out["G3"] = {"trend": tr, "own_beats_ext_share_by_level": share, "m3_n4000_build_beats_update": hits,
                     "units_reaching_4000": len(reach),
                     "a": tr["p_one_sided"] < 0.05 and tr["z"] > 0, "b": len(reach) > 0 and len(hits) >= len(reach) / 2}
        out["G3"]["verdict"] = "holds" if (out["G3"]["a"] and out["G3"]["b"]) else "fails"
    cells = [(k, n, o) for k, u in units.items() if u["set"] in ("T", "M") for n, o in u["by_n"].items() if int(n) >= 1000]
    if cells:
        cv = np.array([o["policies"]["cv"]["regret_mean"] for _, _, o in cells])
        ct = np.array([o["policies"]["closed_test"]["regret_mean"] for _, _, o in cells])
        g4 = {"cells": len(cells), "cv_median": float(np.median(cv)), "cv_p90": float(np.percentile(cv, 90)),
              "cv_le_closed_share": float((cv <= ct).mean())}
        g4["verdict"] = "holds" if (g4["cv_median"] <= 0.002 and g4["cv_p90"] <= 0.005 and
                                    g4["cv_le_closed_share"] >= 0.75) else "fails"
        out["G4"] = g4
    else:
        out["G4"] = {"cells": 0, "verdict": "not evaluable"}
    return out


# =========================================================================== building the units
def externals(st, sy, outcome: str, dest: str, cache: Path, threads: int):
    """The frozen external predictor for `outcome` at destination `dest` (the same models as before)."""
    if outcome == "hypo":
        return st.comp(dest, "lightgbm")
    return P1.external_model(sy, outcome, O_SOURCES[outcome][dest], cache, threads)


def outcome_lm(sy, outcome: str, dest: str):
    if outcome == "hypo":
        return sy.full(dest)
    return sy.outcome(dest, outcome)


def units_H(st, sy, cache, threads, seed):
    from hypo.cv import outer_folds
    lm_all, _ = sy.full("eicu")
    hosp = np.asarray(lm_all.hospital).astype(str)
    subj = np.asarray(lm_all.ft.subjects).astype(str)
    size = {h: np.unique(subj[hosp == h]).size for h in np.unique(hosp)}
    keep = sorted([h for h, n in size.items() if n >= H_MIN_PATIENTS], key=lambda h: -size[h])
    for outcome in ("hypo", "O2"):
        lm_o, _ = outcome_lm(sy, outcome, "eicu")
        try:
            model = externals(st, sy, outcome, "eicu", cache, threads)
        except RuntimeError as e:
            LOG.warning("%s", e)
            continue
        ho = np.asarray(lm_o.hospital).astype(str)
        for i, h in enumerate(keep):
            rows = np.where(ho == h)[0]
            lm = lm_o.take(rows)
            plg = np.clip(np.asarray(model(lm), dtype=np.float64), RA.EPS, 1 - RA.EPS)
            fold = outer_folds(lm, 5, seed + 500 + i)
            yield Unit2(f"H_{outcome}_h{h}", "H", outcome, lm, plg, seed, 100 + 2 * i + (outcome == "O2"), fold=fold)


def anchor_groups(lm) -> np.ndarray:
    import os
    import polars as pl
    base = Path(os.environ.get("PERISIM_DATASETS", "data"))
    p = pl.read_csv(base / "mimic4" / "hosp" / "patients.csv.gz", columns=["subject_id", "anchor_year_group"])
    m = dict(zip(p["subject_id"].to_list(), p["anchor_year_group"].to_list()))
    ids = [int(str(s).split("-")[-1].split(":")[-1]) for s in np.asarray(lm.ft.subjects).astype(str)]
    return np.array([m.get(i) for i in ids], dtype=object)


def units_T(st, sy, cache, threads, seed):
    for j, outcome in enumerate(("hypo", "O1", "O2")):
        lm, _ = outcome_lm(sy, outcome, "mimic")
        g = anchor_groups(lm)
        ok = np.array([x is not None for x in g])
        lm = lm.take(np.where(ok)[0])
        g = g[ok]
        past = np.isin(g, ["2008 - 2010", "2011 - 2013", "2014 - 2016"])
        try:
            model = externals(st, sy, outcome, "mimic", cache, threads)
        except RuntimeError as e:
            LOG.warning("%s", e)
            continue
        plg = np.clip(np.asarray(model(lm), dtype=np.float64), RA.EPS, 1 - RA.EPS)
        yield Unit2(f"T_{outcome}_mimic", "T", outcome, lm, plg, seed, 140 + j,
                    fit_pool=np.where(past)[0], test=np.where(~past)[0])


def units_M(st, sy, cache, threads, seed, only=None):
    k = 0
    for outcome, dests in ROT.items():
        for dest in dests:
            lm, fold = outcome_lm(sy, outcome, dest)
            try:
                model = externals(st, sy, outcome, dest, cache, threads)
            except RuntimeError as e:
                LOG.warning("%s", e)
                continue
            for level in LEVELS:
                name = f"M_{outcome}_{dest}_{level}"
                k += 1
                if only and name not in only and f"M_{outcome}_{dest}" not in only:
                    continue
                plg = np.clip(np.asarray(model(perturb(lm, level)), dtype=np.float64), RA.EPS, 1 - RA.EPS)
                yield Unit2(name, "M", outcome, lm, plg, seed, 200 + k, fold=fold)


# =========================================================================== report
def render(res: dict, hyp: dict) -> str:
    L = ["# Phase 2: update before you build under realistic conditions (pre-registered, OSF " + REGISTRATION + ")", "",
         "Log-loss per landmark on held-out landmarks; samples of n local patients. 'Beats' = lower log-loss in ≥ 80 % "
         "of the samples. Best external = adopt, update or update_tuned; best own = build, build_tuned or build_lr.", "",
         "## Hypotheses", "", "```", json.dumps(hyp, indent=1, default=float), "```", ""]
    for name, r in res.items():
        if "dropped" in r:
            L += [f"## {name}: dropped ({r['dropped']})", ""]
            continue
        d = r["destination"]
        L += [f"## {name}", "", f"{d['patients']:,} patients, {d['landmarks']:,} landmarks, prevalence {d['prevalence']:.3f}. "
              f"Break-even (≥ 80 %): {r['breakeven_80pct']}.", "",
              "| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | "
              "regret cv / closed / v2 | flagged |", "|---|" + "---|" * 9]
        for n, o in r["by_n"].items():
            lm, po = o["logloss_mean"], o["policies"]
            b = o["best_own_vs_best_ext"]
            L.append(f"| {n} | {lm['adopt']:.4f} | {lm['update']:.4f} | {lm['build']:.4f} | {lm['update_tuned']:.4f} | "
                     f"{lm['build_tuned']:.4f} | {lm['build_lr']:.4f} | {b['mean']:+.4f} ({b['share_wins']:.2f}) | "
                     f"{po['cv']['regret_mean']:.4f} / {po['closed_test']['regret_mean']:.4f} / {po['rule_v2']['regret_mean']:.4f} | "
                     f"{o['flag_share']:.2f} |")
        L.append("")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--set", required=True, choices=["H", "T", "M"])
    ap.add_argument("--units", nargs="*", default=None, help="restrict to these unit names (or M_<outcome>_<dest>)")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
                        stream=sys.stdout)
    from hypo.external import Stage
    from hypo.frozen import check, external_dir

    RA.QUICK = a.quick
    RA.PP._logistic = C.logistic_guarded                   # as corrected in the first phase (DECISIONS 2026-11-18)
    check()
    st = Stage(quick=a.quick, threads=a.threads)
    sy = P1.Systems(st)
    od = external_dir().with_name("review")
    ext_cache = od / "units" / "phase1"
    cache = od / "units" / "phase2"
    for d in (ext_cache, cache):
        d.mkdir(parents=True, exist_ok=True)
    cfg, _, _ = RA._cfg()
    seed = int(cfg["seed"])
    gen = {"H": lambda: units_H(st, sy, ext_cache, a.threads, seed),
           "T": lambda: units_T(st, sy, ext_cache, a.threads, seed),
           "M": lambda: units_M(st, sy, ext_cache, a.threads, seed, a.units)}[a.set]
    out_file = od / f"phase2_{a.set}{'_' + '_'.join(a.units) if a.units else ''}.json"
    res = json.loads(out_file.read_text(encoding="utf-8")) if out_file.exists() else {}
    for u in gen():
        if a.units and a.set != "M" and u.name not in a.units:
            continue
        try:
            res[u.name] = run_unit(u, cache, a.threads)
        except Exception as e:                              # a unit that cannot be fitted is reported and kept
            LOG.exception("unit %s failed", u.name)
            res[u.name] = {"dropped": f"{type(e).__name__}: {e}", "set": a.set}
        out_file.write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
        LOG.info("phase2 %s done", u.name)
    allres = {}
    for f in sorted(od.glob("phase2_[HTM]*.json")):
        if f.name.lower() == "phase2_hypotheses.json":      # Windows globs ignore case: [HTM] also matches "h"
            continue
        allres.update(json.loads(f.read_text(encoding="utf-8")))
    hyp = hypotheses(allres)
    (od / "phase2_hypotheses.json").write_text(json.dumps(hyp, indent=1, default=float), encoding="utf-8")
    rep = external_dir().parent / "reports" / "phase2_realism.md"
    rep.write_text(render(allres, hyp), encoding="utf-8")
    LOG.info("phase2: %s", rep)
    check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
