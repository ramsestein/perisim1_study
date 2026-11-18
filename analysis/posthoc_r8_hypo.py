"""Post hoc, EXPLORATORY: internal review 8 on `hypo` (docs/DECISIONS.md, 2026-11-17, R5–R7).

Same samples as review 7 (draws, folds, seeds): the three options refitted (review 7 kept no predictions), the
closed testing procedure of Vergouwe et al. (2017) as adapted in `roll`, net benefit at 0.10/0.20/0.30, events, two
more own-model arms (LightGBM tuned by inner CV; L2 logistic regression) and the Riley et al. (2020) minimum sample
size per destination. The cross-validated choice and the rule are read from review 7's records when present.

Usage:  python scripts/posthoc_r8_hypo.py [--units inspire mimic eicu nwicu] [--threads 8]
Outputs (aggregates only): <experiments>/hypo/review/r8_<unit>.json and reports/r8_hypo.md
"""

from __future__ import annotations

import argparse
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
import own_ext_common as C  # noqa: E402

LOG = logging.getLogger("r8")
THRESHOLDS = (0.10, 0.20, 0.30)
GRID = [(nl, md) for nl in (7, 15, 31) for md in (20, 100)]
C_GRID = (0.01, 0.1, 1.0)


def lgbm_params(X, y, subj, X_te, cat_idx, seed, threads, num_leaves=31, min_data=50, init=None, init_te=None):
    """RA.lgbm_local with num_leaves and min_data_in_leaf as arguments (R7)."""
    import lightgbm as lgb
    y = np.asarray(y, dtype=np.float64)
    base = 0.0 if init_te is None else init_te
    if y.min() == y.max():
        return RA.sigmoid(base + (RA.logit(np.full(X_te.shape[0], y.mean())) if init_te is None else 0.0))
    uniq = np.unique(subj)
    rng = np.random.default_rng(seed)
    va = np.isin(subj, rng.choice(uniq, size=max(1, int(round(0.2 * uniq.size))), replace=False))
    fi = ~va
    if y[fi].min() == y[fi].max():
        fi = va = np.ones(y.size, dtype=bool)
    params = {"objective": "binary", "learning_rate": 0.05, "num_leaves": num_leaves, "min_data_in_leaf": min_data,
              "bagging_fraction": 0.8, "bagging_freq": 1, "feature_fraction": 0.8, "deterministic": True,
              "force_col_wise": True, "num_threads": threads, "seed": seed, "verbose": -1}
    dtr = lgb.Dataset(X[fi], y[fi], init_score=None if init is None else init[fi], categorical_feature=cat_idx,
                      free_raw_data=False)
    dva = lgb.Dataset(X[va], y[va], init_score=None if init is None else init[va], reference=dtr,
                      categorical_feature=cat_idx)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        b = lgb.train(params, dtr, 2000, valid_sets=[dva], callbacks=[lgb.early_stopping(50, verbose=False)])
    it = int(b.best_iteration or b.current_iteration())
    return RA.sigmoid(base + b.predict(X_te, num_iteration=it, raw_score=True))


def own_tuned(X, y, subj, fit, te, cat_idx, seed, threads):
    from sklearn.model_selection import GroupKFold
    score = {}
    for g in GRID:
        s = 0.0
        for i, (a, b) in enumerate(GroupKFold(C.INNER).split(fit, groups=subj[fit])):
            p = lgbm_params(X[fit[a]], y[fit[a]], subj[fit[a]], X[fit[b]], cat_idx, seed + 7 * i, threads, *g)
            s += float(RA.PP.ll_rows(p, y[fit[b]]).sum())
        score[g] = s
    g = min(score, key=score.get)
    return lgbm_params(X[fit], y[fit], subj[fit], X[te], cat_idx, seed, threads, *g), {"num_leaves": g[0], "min_data": g[1]}


class Design:
    """R7's logistic design, fitted on the sample: medians, missing indicators, one-hot categories, standardised."""

    def __init__(self, X, cat_idx):
        self.cat = list(cat_idx)
        self.num = [j for j in range(X.shape[1]) if j not in self.cat]
        N = X[:, self.num]
        self.med = np.nanmedian(np.where(np.isfinite(N), N, np.nan), axis=0)
        self.med = np.where(np.isfinite(self.med), self.med, 0.0)
        self.miss = [k for k in range(N.shape[1]) if (~np.isfinite(N[:, k])).any()]
        self.levels = [np.unique(X[np.isfinite(X[:, j]), j]) for j in self.cat]
        Z = self._raw(X)
        self.mu, self.sd = Z.mean(0), Z.std(0)
        self.sd[self.sd == 0] = 1.0

    def _raw(self, X):
        N = X[:, self.num]
        M = ~np.isfinite(N)
        N = np.where(M, self.med, N)
        cols = [N, M[:, self.miss].astype(float)]
        for j, lv in zip(self.cat, self.levels):
            cols.append((X[:, j][:, None] == lv[None, :]).astype(float))
        return np.hstack(cols)

    def __call__(self, X):
        return (self._raw(X) - self.mu) / self.sd


def own_lr(X, y, subj, fit, te, cat_idx, seed):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    if y[fit].min() == y[fit].max():
        return np.full(te.size, y[fit].mean()), {"C": None}
    score = {}
    for c in C_GRID:
        s = 0.0
        for a, b in GroupKFold(C.INNER).split(fit, groups=subj[fit]):
            d = Design(X[fit[a]], cat_idx)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                m = LogisticRegression(C=c, max_iter=2000).fit(d(X[fit[a]]), y[fit[a]])
            s += float(RA.PP.ll_rows(m.predict_proba(d(X[fit[b]]))[:, 1], y[fit[b]]).sum())
        score[c] = s
    c = min(score, key=score.get)
    d = Design(X[fit], cat_idx)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = LogisticRegression(C=c, max_iter=2000).fit(d(X[fit]), y[fit])
    return np.clip(m.predict_proba(d(X[te]))[:, 1], RA.EPS, 1 - RA.EPS), {"C": c}


def closed_test(Xraw, cat_idx, plg, y, subj, fit, seed, threads) -> str:
    pats = np.unique(subj[fit])
    rng = np.random.default_rng(seed + 11)
    fp = np.isin(subj[fit], rng.permutation(pats)[:int(round(2 / 3 * pats.size))])
    f, v = fit[fp], fit[~fp]
    lp = RA.logit(plg)
    P = {"keep": plg[v], "intercept": RA.recal("intercept", plg[f], y[f], plg[v]),
         "logistic": RA.recal("logistic", plg[f], y[f], plg[v]),
         "update": RA.lgbm_local(Xraw[f], y[f], subj[f], Xraw[v], cat_idx, seed + 13, threads, init=lp[f], init_te=lp[v])[0],
         "own": RA.lgbm_local(Xraw[f], y[f], subj[f], Xraw[v], cat_idx, seed + 13, threads)[0]}
    L = {k: RA.PP.ll_rows(p, y[v]) for k, p in P.items()}
    return C.closed_choice(L, subj[v])


def riley_unit(u, Xraw, cat_idx) -> dict:
    y = u.y.astype(np.float64)
    plg = u.P["lgbm_transported"]
    p = np.full(y.size, np.nan)
    for f in u.folds:
        tr, te = u.split(f)
        p[te] = RA.recal("logistic", plg[tr], y[tr], plg[te])
    phi = float(y.mean())
    ll_null = float(-(phi * np.log(phi) + (1 - phi) * np.log(1 - phi)))
    r2 = C.r2cs_from_logloss(OE.ll(p, y), ll_null)
    width = Design(Xraw[np.random.default_rng(0).choice(y.size, size=min(50000, y.size), replace=False)], cat_idx)
    p_par = int(width(Xraw[:2]).shape[1])
    out = C.riley_n(p_par, phi, r2)
    lm_per_patient = y.size / np.unique(u.subj).size
    out.update({"landmarks_per_patient": float(lm_per_patient), "n_patients": float(np.ceil(out["n"] / lm_per_patient)),
                "note": "per landmark, converted to patients; regression parameters = width of the logistic design"})
    return out


def run_unit(u, units: Path, threads: int) -> dict:
    y = u.y.astype(np.float64)
    plg = u.P["lgbm_transported"]
    Xraw, cat_idx = RA.raw_matrix(u.lm, RA.cat_levels(u.lm))
    n_pat_min = min(np.unique(u.subj[u.split(f)[0]]).size for f in u.folds)
    sizes = [n for n in OE.SIZES if n < n_pat_min]
    old, cache = units / "own_vs_external", units / "r8"
    cache.mkdir(exist_ok=True)
    samples = []
    for n in sizes:
        for r in range(OE.DRAWS[n]):
            for f in u.folds:
                path = cache / f"{u.name}_n{n}_r{r}_f{f}.json"
                if path.exists():
                    samples.append(json.loads(path.read_text(encoding="utf-8")))
                    continue
                t0 = time.perf_counter()
                tr, te = u.split(f)
                fit = tr[u.draw(f, tr, int(n), r)]
                seed = u.seed + 100 * f + 17 * r + n                          # review 7's seed
                P = OE.options(Xraw, cat_idx, plg, y, u.subj, fit, te, seed, threads)
                P["keep"] = plg[te]
                P["intercept"] = RA.recal("intercept", plg[fit], y[fit], plg[te])
                P["logistic"] = P["adopt"]
                P["own_tuned"], tuned = own_tuned(Xraw, y, u.subj, fit, te, cat_idx, seed, threads)
                P["own_lr"], lrinfo = own_lr(Xraw, y, u.subj, fit, te, cat_idx, seed)
                op = old / f"{u.name}_n{n}_r{r}_f{f}.json"
                if op.exists():
                    o7 = json.loads(op.read_text(encoding="utf-8"))
                    cv, rule = o7["cv_choice"], o7["rule_choice"]
                else:
                    cv, _ = OE.cv_choice(Xraw, cat_idx, plg, y, u.subj, fit, seed, threads)
                    rule = C.rule_choice(OE.diagnostics(plg[fit], y[fit], seed + 3), n)
                ct = closed_test(Xraw, cat_idx, plg, y, u.subj, fit, seed, threads)
                L = {a: OE.ll(p, y[te]) for a, p in P.items()}
                L["own_best"] = min(L[v] for v in C.OWN_VARIANTS)
                bestv = min(C.OWN_VARIANTS, key=lambda v: L[v])
                nb = {f"t{t:.2f}": {a: C.net_benefit(P[a], y[te], t) for a in ("adopt", "update", "own")} | {
                    "own_best": C.net_benefit(P[bestv], y[te], t)} for t in THRESHOLDS}
                ev_pat = int(np.unique(u.subj[fit][y[fit] == 1]).size)
                rec = {"n": n, "r": r, "f": int(f), "ll": L, "cv_choice": cv, "rule_choice": rule, "closed_choice": ct,
                       "nb": nb, "events": {"landmarks": int(y[fit].sum()), "patients": ev_pat},
                       "tuned": tuned, "lr": lrinfo, "seconds": time.perf_counter() - t0}
                path.write_text(json.dumps(rec), encoding="utf-8")
                samples.append(rec)
                LOG.info("r8 %s n=%d r=%d f%d: closed→%s, cv→%s (%.0f s)", u.name, n, r, f, ct, cv, rec["seconds"])
    out = C.summarise_r8(samples, sizes, [f"t{t:.2f}" for t in THRESHOLDS])
    out.update({"unit": u.name, "sizes": sizes, "riley": riley_unit(u, Xraw, cat_idx)})
    return out


def render(res: dict) -> str:
    L = ["# Internal review 8 on `hypo` (post hoc, exploratory)", ""]
    for name, r in res.items():
        rl = r["riley"]
        L += [f"## {name}", "", f"Break-even (≥ 80 % of samples): {r['breakeven_80pct']}",
              f"Riley et al. (2020) for a regression model: n = {rl['n']:.0f} landmarks ≈ {rl['n_patients']:.0f} patients "
              f"({rl['events']:.0f} events; p = {rl['p']}, R²cs {rl['r2cs']:.3f}, prevalence {rl['prevalence']:.3f})", "",
              "| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | "
              "ΔNB own − adopt /100 (0.10, 0.20, 0.30) | events (landmarks, patients) |", "|---|---|---|---|---|---|---|"]
        for n, o in r["by_n"].items():
            po = o["policies"]
            nb = o["net_benefit"]
            L.append(f"| {n} | {po['cv']['regret_mean']:.4f} / {po['closed_test']['regret_mean']:.4f} / {po['rule']['regret_mean']:.4f} | "
                     f"{po['cv']['correct_share']:.2f} / {po['closed_test']['correct_share']:.2f} / {po['rule']['correct_share']:.2f} | "
                     f"{po['closed_test']['chosen_share']} | "
                     + ", ".join(f"{o[f'{v}_vs_adopt']['mean']:+.4f} ({o[f'{v}_vs_adopt']['share_wins']:.2f})"
                                 for v in C.OWN_VARIANTS + ('own_best',)) + " | "
                     + ", ".join(f"{nb[f't{t:.2f}|own_vs_adopt']['mean_per_100']:+.2f}" for t in THRESHOLDS) + " | "
                     f"{o['events_mean']['landmarks']:.0f}, {o['events_mean']['patients']:.0f} |")
        L.append("")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--units", nargs="*", default=list(RA.ROTATIONS) + ["nwicu"])
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
                        stream=sys.stdout)
    from hypo.external import Stage
    from hypo.frozen import check, external_dir

    RA.QUICK = a.quick
    check()
    st = Stage(quick=a.quick, threads=a.threads)
    od = external_dir().with_name("review")
    units = od / "units"
    units.mkdir(parents=True, exist_ok=True)
    cache = {}
    for X in a.units:
        U = [RA.unit_nwicu(st, e, cache) for e in RA.ROTATIONS] if X == "nwicu" else [RA.unit_hypo(st, X)]
        res = {}
        for u in U:
            res[u.name] = run_unit(u, units, a.threads)
            (od / f"r8_{X}.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
        LOG.info("r8 %s done", X)
    allres = {}
    for f in sorted(od.glob("r8_*.json")):
        allres.update(json.loads(f.read_text(encoding="utf-8")))
    rep = external_dir().parent / "reports" / "r8_hypo.md"
    rep.write_text(render(allres), encoding="utf-8")
    LOG.info("r8: %s", rep)
    check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
