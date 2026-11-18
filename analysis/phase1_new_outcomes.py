"""Phase 1 of docs/prereg_third_outcome.md (registered: OSF 10.17605/OSF.IO/YPBVH, 2026-11-17): adopt, update or
build on two outcomes not analysed before, with the decision procedures fixed in the registration.

Outcomes (carried by the `hypo` landmarks): O1 `vaso_start` among landmarks with no vasopressor running at L
(MIMIC-IV, eICU-CRD, NWICU); O2 `icu_discharge_24h` (INSPIRE, MIMIC-IV, eICU-CRD, NWICU).
For each destination, an external LightGBM is fitted on the source systems exactly as `hypo`'s transported LightGBM
(`compare.fit("lightgbm")`, the frozen seed) and frozen; then, as internal reviews 7 and 8, within each of the
destination's 5 patient folds and each draw of n local patients: adopt (logistic recalibration), update (LightGBM
boosted from the external model), own (LightGBM from scratch, fixed settings), own_tuned, own_lr, keep and intercept
are fitted on the n patients and scored on the fold's test landmarks; the CV choice, the closed test, rule v1 and
rule v2 are read on the same n patients. H1–H3 are evaluated as registered (section 4).

Usage:  python scripts/phase1_new_outcomes.py [--units O1:mimic O2:nwicu ...] [--threads 4]
Outputs (aggregates only): <experiments>/hypo/review/phase1_<O>_<dest>.json and reports/phase1_new_outcomes.md
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_analyses as RA  # noqa: E402
import posthoc_own_vs_external as OE  # noqa: E402
import posthoc_r8_hypo as R8  # noqa: E402
import own_ext_common as C  # noqa: E402

LOG = logging.getLogger("phase1")
REGISTRATION = "10.17605/OSF.IO/YPBVH"
COLUMN = {"O1": "vaso_start", "O2": "icu_discharge_24h"}
NB_T = {"O1": (0.05, 0.10, 0.20), "O2": (0.30, 0.50, 0.70)}
# destination → source systems of its external model (registration section 3)
PLAN = {"O1": {"mimic": [("eicu",)], "eicu": [("mimic",)], "nwicu": [("mimic", "eicu")]},
        "O2": {"inspire": [("mimic", "eicu")], "mimic": [("inspire", "eicu")], "eicu": [("inspire", "mimic")],
               "nwicu": [("mimic", "eicu"), ("inspire", "eicu"), ("inspire", "mimic")]}}
CI_BASE = {"O1": 20, "O2": 40}


def all_units() -> list[str]:
    return [f"{o}:{d}" for o in PLAN for d in PLAN[o]]


# =========================================================================== landmarks with the new outcome
def off_vasopressor(lm) -> np.ndarray:
    if "vaso_on" in lm.ft.num:
        return np.asarray(lm.ft.num["vaso_on"], dtype=np.float64) == 0.0
    to = {"0": True, "false": True, "no": True}
    return np.array([to.get(str(v).strip().lower().replace(".0", ""), False) for v in lm.ft.cat["vaso_on"]])


def outcome_rows(lm, outcome: str) -> tuple[np.ndarray, np.ndarray]:
    """Rows of the outcome's population and their labels (registration section 2)."""
    import polars as pl
    v = lm.frame[COLUMN[outcome]].cast(pl.Float64).to_numpy()
    keep = np.isfinite(v)
    if outcome == "O1":
        keep &= off_vasopressor(lm)
    rows = np.where(keep)[0]
    return rows, v[rows].astype(np.int64)


def with_outcome(lm, outcome: str):
    rows, y = outcome_rows(lm, outcome)
    return dataclasses.replace(lm.take(rows), y=y), rows


class OUnit:
    """What review 7 and 8's helpers read from a unit: landmarks, folds, labels, the external model's predictions."""

    def __init__(self, name, lm, fold, plg, seed, ci, sources):
        self.name, self.lm, self.fold, self.seed, self.ci, self.sources = name, lm, fold, seed, ci, sources
        self.P = {"lgbm_transported": plg}
        self.y = lm.y.astype(np.int64)
        self.subj = np.asarray(lm.ft.subjects).astype(str)

    @property
    def folds(self):
        return sorted(set(self.fold.tolist()))

    def split(self, f):
        return np.where(self.fold != f)[0], np.where(self.fold == f)[0]

    def draw(self, f: int, tr: np.ndarray, n: int, r: int) -> np.ndarray:
        s = self.subj[tr]
        uniq = np.unique(s)
        rng = np.random.default_rng([int(self.seed), 7, self.ci, f, n, r])
        pick = rng.choice(uniq, size=min(n, uniq.size), replace=False)
        return np.where(np.isin(s, pick))[0]


class Systems:
    """Landmarks and outer folds of the four systems (the frozen `hypo` folds; NWICU's as nwicu_transport)."""

    def __init__(self, st):
        self.st, self._lm, self._fold = st, {}, {}

    def full(self, c: str):
        if c not in self._lm:
            if c == "nwicu":
                import nwicu_transport as NT
                from hypo.cv import outer_folds
                cfg, _, _ = RA._cfg()
                lm = NT.landmarks(cfg)
                self._lm[c], self._fold[c] = lm, outer_folds(lm, int(cfg["cv"]["outer_folds"]), int(cfg["seed"]))
            else:
                self._lm[c], self._fold[c] = self.st.S.lm(c), self.st.S.fold(c)
        return self._lm[c], self._fold[c]

    def outcome(self, c: str, outcome: str):
        lm, fold = self.full(c)
        lo, rows = with_outcome(lm, outcome)
        return lo, fold[rows]


def external_model(sy: Systems, outcome: str, sources: tuple, cache: Path, threads: int):
    """The external LightGBM of `outcome` fitted on `sources` as `hypo`'s transported LightGBM (frozen once)."""
    from hypo import compare
    from hypo.config import code_hash
    from hypo.data import concat
    from hypo.frozen import dump, load_pickle
    path = cache / f"ext_{outcome}_{'+'.join(sources)}.pkl"
    if not path.exists():
        cfg, mcfg, space = RA._cfg()
        pool = concat([sy.outcome(c, outcome)[0] for c in sources])
        ev = int(pool.y.sum())
        if ev < 100:
            raise RuntimeError(f"{outcome} from {sources}: {ev} events in the source (< 100): unit dropped")
        seed = int(cfg["seed"]) + int(cfg["external"]["final_seed_offset"])
        t = time.perf_counter()
        pred, info = compare.fit("lightgbm", pool, mcfg, space["baselines"], n_inner=int(cfg["cv"]["inner_folds"]),
                                 seed=seed, threads=threads)
        info = {"outcome": outcome, "sources": list(sources), "n_train": len(pool), "events": ev, "seed": seed,
                "code_hash": code_hash(), "seconds": time.perf_counter() - t, "registration": REGISTRATION, **info}
        path.with_suffix(".json").write_text(json.dumps(info, indent=1, default=float), encoding="utf-8")
        dump(pred, path)
        LOG.info("external %s from %s: %d landmarks, %d events, %.0f s", outcome, "+".join(sources), len(pool), ev,
                 info["seconds"])
    return load_pickle(path)


# =========================================================================== one sample and one unit
def sample(u: OUnit, Xraw, cat_idx, fit, te, n: int, seed: int, thresholds, threads: int) -> dict:
    y = u.y.astype(np.float64)
    plg = u.P["lgbm_transported"]
    P = OE.options(Xraw, cat_idx, plg, y, u.subj, fit, te, seed, threads)
    P["keep"] = plg[te]
    P["intercept"] = RA.recal("intercept", plg[fit], y[fit], plg[te])
    P["own_tuned"], tuned = R8.own_tuned(Xraw, y, u.subj, fit, te, cat_idx, seed, threads)
    P["own_lr"], lrinfo = R8.own_lr(Xraw, y, u.subj, fit, te, cat_idx, seed)
    cv, cvl = OE.cv_choice(Xraw, cat_idx, plg, y, u.subj, fit, seed, threads)
    dg = OE.diagnostics(plg[fit], y[fit], seed + 3)
    ct = R8.closed_test(Xraw, cat_idx, plg, y, u.subj, fit, seed, threads)
    L = {a: OE.ll(p, y[te]) for a, p in P.items()}
    L["logistic"] = L["adopt"]                  # the closed test's "logistic" is adopt (same recalibration)
    L["own_best"] = min(L[v] for v in C.OWN_VARIANTS)
    bestv = min(C.OWN_VARIANTS, key=lambda v: L[v])
    nb = {f"t{t:.2f}": {a: C.net_benefit(P[a], y[te], t) for a in ("adopt", "update", "own")}
          | {"own_best": C.net_benefit(P[bestv], y[te], t)} for t in thresholds}
    return {"ll": L, "auc": {a: OE.auc(P[a], y[te]) for a in C.OPTIONS + ("own_tuned", "own_lr", "keep")},
            "cv_choice": cv, "cv_logloss": cvl, "diag": dg, "relation_shift": C.relation_shift(dg),
            "rule_choice": C.rule_choice(dg, n), "rule_v2_choice": C.rule_v2_choice(dg, n), "closed_choice": ct,
            "nb": nb, "events": {"landmarks": int(y[fit].sum()), "patients": int(np.unique(u.subj[fit][y[fit] == 1]).size)},
            "tuned": tuned, "lr": lrinfo}


def run_unit(u: OUnit, cache: Path, thresholds, threads: int) -> dict:
    Xraw, cat_idx = RA.raw_matrix(u.lm, RA.cat_levels(u.lm))
    n_pat_min = min(np.unique(u.subj[u.split(f)[0]]).size for f in u.folds)
    sizes = [n for n in OE.SIZES if n < n_pat_min]
    samples = []
    for n in sizes:
        for r in range(OE.DRAWS[n]):
            for f in u.folds:
                path = cache / f"{u.name}_n{n}_r{r}_f{f}.json"
                if path.exists():
                    rec = json.loads(path.read_text(encoding="utf-8"))
                    rec["ll"].setdefault("logistic", rec["ll"]["adopt"])   # records written before the alias
                    samples.append(rec)
                    continue
                t0 = time.perf_counter()
                tr, te = u.split(f)
                fit = tr[u.draw(f, tr, int(n), r)]
                rec = {"n": n, "r": r, "f": int(f), "test_rows": int(te.size)}
                rec.update(sample(u, Xraw, cat_idx, fit, te, n, u.seed + 100 * f + 17 * r + n, thresholds, threads))
                rec["seconds"] = time.perf_counter() - t0
                path.write_text(json.dumps(rec, default=float), encoding="utf-8")
                samples.append(rec)
                LOG.info("phase1 %s n=%d r=%d f%d: cv→%s, closed→%s, v2→%s (%.0f s)", u.name, n, r, f,
                         rec["cv_choice"], rec["closed_choice"], rec["rule_v2_choice"], rec["seconds"])
    out = C.summarise_r8(samples, sizes, [f"t{t:.2f}" for t in thresholds])
    C.add_policy(out, samples, "rule_v2", "rule_v2_choice")
    out["hypotheses"] = C.hypotheses(samples, out, sizes)
    y = u.y
    out.update({"unit": u.name, "sources": list(u.sources), "sizes": sizes, "riley": R8.riley_unit(u, Xraw, cat_idx),
                "destination": {"landmarks": int(y.size), "patients": int(np.unique(u.subj).size),
                                "prevalence": float(y.mean()), "events": int(y.sum())},
                "auroc_mean": {str(n): {a: float(np.nanmean([s["auc"][a] for s in samples if s["n"] == n]))
                                        for a in samples[0]["auc"]} for n in sizes},
                "registration": REGISTRATION})
    return out


# =========================================================================== report
def render(res: dict) -> str:
    L = ["# Phase 1: adopt, update or build on two new outcomes (pre-registered, OSF " + REGISTRATION + ")", "",
         "Log-loss per landmark on each fold's test landmarks; one sample = one draw of n local patients in one fold. "
         "Regret against the best of adopt, update and own. Break-even: smallest n with ≥ 80 % of samples won.", ""]
    for name, r in res.items():
        h, d, rl = r["hypotheses"], r["destination"], r["riley"]
        L += [f"## {name} (external model from {' + '.join(r['sources'])})", "",
              f"Destination: {d['landmarks']:,} landmarks, {d['patients']:,} patients, prevalence {d['prevalence']:.3f}.",
              f"Regime label: {h['regime']} ({h['flag_share']:.2f} of samples with n ≤ 1,000 flagged). "
              f"Break-even (≥ 80 %): {r['breakeven_80pct']}.",
              f"H1: {h['H1']}; H2: {h['H2']}; H3: {h['H3']}.",
              f"Riley et al. (2020): n = {rl['n']:.0f} landmarks ≈ {rl['n_patients']:.0f} patients "
              f"(p = {rl['p']}, R²cs {rl['r2cs']:.3f}).", "",
              "| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | "
              "closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |", "|---|" + "---|" * 10]
        for n, o in r["by_n"].items():
            lm, po, nb = o["logloss_mean"], o["policies"], o["net_benefit"]
            ks = ("cv", "closed_test", "rule", "rule_v2")
            L.append(f"| {n} | {lm['adopt']:.4f} | {lm['update']:.4f} | {lm['own']:.4f} | {lm['own_tuned']:.4f} | "
                     f"{lm['own_lr']:.4f} | " + " / ".join(f"{po[k]['regret_mean']:.4f}" for k in ks) + " | "
                     + " / ".join(f"{po[k]['correct_share']:.2f}" for k in ks) + f" | {po['closed_test']['chosen_share']} | "
                     + ", ".join(f"{v['mean_per_100']:+.2f}" for k, v in nb.items() if k.endswith("|own_vs_adopt"))
                     + f" | {o['events_mean']['landmarks']:.0f}, {o['events_mean']['patients']:.0f} |")
        L.append("")
    L += ["## Confirmatory summary", "", "| hypothesis | units holding | units failing | not evaluable | verdict |",
          "|---|---|---|---|---|"]
    for k, v in C.verdicts([r["hypotheses"] for r in res.values()]).items():
        L.append(f"| {k} | {v['hold']} | {v['fail']} | {v['not_evaluable']} | {v['verdict']} |")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--units", nargs="*", default=all_units())
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--cache", default="v1", help="sample cache; v2 = after the guarded recalibration (2026-11-18)")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
                        stream=sys.stdout)
    from hypo.external import Stage
    from hypo.frozen import check, external_dir

    RA.QUICK = a.quick
    RA.PP._logistic = C.logistic_guarded          # DECISIONS 2026-11-18: plain Newton diverged in O2_inspire
    check()
    st = Stage(quick=a.quick, threads=a.threads)
    sy = Systems(st)
    od = external_dir().with_name("review")
    cache = od / "units" / ("phase1" if a.cache == "v1" else f"phase1_{a.cache}")
    cache.mkdir(parents=True, exist_ok=True)
    cfg, _, _ = RA._cfg()
    for key in a.units:
        outcome, dest = key.split(":")
        lm, fold = sy.outcome(dest, outcome)
        res = {}
        for i, sources in enumerate(PLAN[outcome][dest]):
            name = f"{outcome}_{dest}" + (f"_from_{'+'.join(sources)}" if len(PLAN[outcome][dest]) > 1 else "")
            try:
                model = external_model(sy, outcome, sources, od / "units" / "phase1", a.threads)
            except RuntimeError as e:
                LOG.warning("%s", e)
                res[name] = {"dropped": str(e)}
                (od / f"phase1_{outcome}_{dest}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
                continue
            plg = np.clip(np.asarray(model(lm), dtype=np.float64), RA.EPS, 1 - RA.EPS)
            ci = CI_BASE[outcome] + 4 * list(PLAN[outcome]).index(dest) + i
            u = OUnit(name, lm, fold, plg, int(cfg["seed"]), ci, sources)
            res[name] = run_unit(u, cache, NB_T[outcome], a.threads)
            (od / f"phase1_{outcome}_{dest}.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
        LOG.info("phase1 %s done", key)
    allres = {}
    for f in sorted(od.glob("phase1_O*_*.json")):
        allres.update({k: v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if "dropped" not in v})
    rep = external_dir().parent / "reports" / "phase1_new_outcomes.md"
    rep.write_text(render(allres), encoding="utf-8")
    LOG.info("phase1: %s", rep)
    check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
