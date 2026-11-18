"""Post hoc, EXPLORATORY: adopt, update or build? on T2 (docs/DECISIONS.md, 2026-11-17, internal review 7, R3).

R2's draws of n local pool patients (MIMIC-IV, eICU; development INSPIRE) and its fixed test set: *adopt* = the
transported LightGBM with multinomial recalibration of offsets + common slope, *update* = multiclass LightGBM
boosted from it, *own* = multiclass LightGBM from scratch (R2's cached test predictions). New here: the hospital's
choice by a 3-fold patient-grouped cross-validation on its n patients, and the shift diagnostics on those patients
(recalibration slope; expected − observed macro AUROC).

Usage:  python scripts/posthoc_t2_own.py [--profile local] [--threads 8]
Outputs (aggregates only): <workdir>/experiments/t2/results/posthoc/t2_own.json and reports/t2_own.md
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import posthoc_t2_ladder as LD  # noqa: E402  (sets the frozen src on sys.path)
import own_ext_common as OE  # noqa: E402

PT = LD.PT
from perisim.transport.core import macro_auroc  # noqa: E402

LOG = logging.getLogger("t2_own")
SIZES = (250, 500, 1000, 2000, 4000, 8000)
MAP = {"adopt": "offsets_slope", "update": "warm", "own": "scratch"}


def t2_options(P_all, Xm, y, sX, C, fit, q, seed, threads) -> dict:
    a, b = PT.fit_recal(P_all[fit], y[fit], slope=True)
    Lf, Lq = np.log(np.clip(P_all[fit], LD.EPS, 1)), np.log(np.clip(P_all[q], LD.EPS, 1))
    return {"adopt": PT.apply_recal(P_all[q], a, b),
            "update": LD.lgbm_multi(Xm[fit], y[fit], sX[fit], Xm[q], C, seed, threads, init=Lf, init_te=Lq),
            "own": LD.lgbm_multi(Xm[fit], y[fit], sX[fit], Xm[q], C, seed, threads)}


def t2_diag(P, y, seed) -> dict:
    _, slope = PT.fit_recal(P, y, slope=True)
    off0, _ = PT.fit_recal(P, y, slope=False)
    Prec = PT.apply_recal(P, off0, 1.0)
    rng = np.random.default_rng(seed)
    exp = []
    for _ in range(20):
        ys = (rng.random(len(Prec))[:, None] > np.cumsum(Prec, 1)).sum(1)
        ys = np.minimum(ys, Prec.shape[1] - 1)
        if np.unique(ys).size == Prec.shape[1]:
            exp.append(macro_auroc(Prec, ys))
    obs = macro_auroc(P, y) if np.unique(y).size == P.shape[1] else float("nan")
    e = float(np.mean(exp)) if exp else float("nan")
    return {"slope": float(slope), "auroc_observed": float(obs), "auroc_expected": e, "auroc_gap": float(e - obs)}


def run(pipe, threads: int) -> int:
    from sklearn.model_selection import GroupKFold
    cfg, ws = pipe.cfg, pipe.ws
    t = "t2"
    dev = cfg.experiment["cohorts"]["development"]
    externals = [c for c in cfg.experiment["cohorts"]["external"] if c in pipe.available_cohorts()]
    args = {"names": pipe.feature_names(), "dev": dev, "externals": externals, "threads": threads}
    lcache = ws.predictions("posthoc", t) / "ladder"
    cache = ws.predictions("posthoc", t) / "own"
    cache.mkdir(parents=True, exist_ok=True)
    fm = PT._load(ws.predictions("external", t) / "final_model.pkl")
    enc = fm["enc"]
    ins = None
    out = {"note": "Exploratory, post hoc (internal review 7, 2026-11-17).", "cohorts": {}}
    for c in externals:
        if PT._eval_target_for(t, c, cfg) != t:
            continue
        ctx = PT.context(cfg, ws, t, c, args)
        X, C, y, split = ctx["X"], ctx["C"], ctx["lab"]["own"], ctx["split"]
        q, pool = (v[y[v] >= 0] for v in (split["test"], split["pool"]))
        sX = X.ft.subjects.astype(str)
        Xm = enc.transform_model(X.ft)[0]
        pp = lcache / f"{c}_P_transported.npy"
        if pp.exists():
            P_all = np.load(pp)
        else:
            ins = ins or PT.inspire_models(cfg, ws, t, args)
            P_all = ins["models"]["lgbm"](Xm)
        pats = np.unique(sX[pool])
        sizes = [n for n in SIZES if n < pats.size]
        samples = []
        for n in sizes:
            for r in range(LD.DRAWS[n]):
                path = cache / f"{c}_n{n}_r{r}.json"
                if path.exists():
                    samples.append(json.loads(path.read_text(encoding="utf-8")))
                    continue
                t0 = time.perf_counter()
                seed = int(ctx["seed"]) + 1000 * r + int(n)               # R2's draw
                pick = np.random.default_rng(seed).choice(pats, size=int(n), replace=False)
                fit = pool[np.isin(sX[pool], pick)]
                lp = lcache / f"{c}_n{n}_r{r}.npz"
                if lp.exists():
                    z = np.load(lp, allow_pickle=True)
                    P = {o: z[a] for o, a in MAP.items()}
                else:
                    P = t2_options(P_all, Xm, y, sX, C, fit, q, seed, threads)
                L = {o: 0.0 for o in OE.OPTIONS}
                for i, (a_, b_) in enumerate(GroupKFold(OE.INNER).split(fit, groups=sX[fit])):
                    Pi = t2_options(P_all, Xm, y, sX, C, fit[a_], fit[b_], seed + 31 * (i + 1), threads)
                    for o in OE.OPTIONS:
                        L[o] += -float(np.sum(np.log(np.clip(Pi[o][np.arange(b_.size), y[fit[b_]]], LD.EPS, 1))))
                ch = min(OE.OPTIONS, key=lambda o: L[o])
                dg = t2_diag(P_all[fit], y[fit], seed + 3)
                rec = {"n": n, "r": r, "ll": {o: LD.logloss(P[o], y[q]) for o in OE.OPTIONS},
                       "auc": {o: macro_auroc(P[o], y[q]) for o in OE.OPTIONS},
                       "cv_choice": ch, "cv_logloss": {o: v / fit.size for o, v in L.items()}, "diag": dg,
                       "rule_choice": OE.rule_choice(dg, n), "seconds": time.perf_counter() - t0}
                path.write_text(json.dumps(rec), encoding="utf-8")
                samples.append(rec)
                LOG.info("t2 own %s n=%d r=%d: cv→%s (%.0f s)", c, n, r, ch, rec["seconds"])
        res = OE.summarise(samples, sizes)
        res.update({"sizes": sizes, "draws": {str(n): LD.DRAWS[n] for n in sizes}, "test_rows": int(q.size),
                    "pool_patients": int(pats.size)})
        out["cohorts"][c] = res
        LOG.info("t2 own %s done", c)
    rd = ws.root / "results" / "posthoc"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "t2_own.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    (ws.reports / "t2_own.md").write_text(OE.render({f"t2_{c}": v for c, v in out["cohorts"].items()}),
                                          encoding="utf-8")
    LOG.info("t2 own: %s", rd / "t2_own.json")
    return 0


def main(argv=None) -> int:
    from perisim.config import load_config
    from perisim.pipeline import Pipeline
    from perisim.utils import now_iso, setup_logging

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--profile", default=None)
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--threads", type=int, default=8)
    a = ap.parse_args(argv)
    over = {"experiment": {"paths": {"workdir": str(Path(a.workdir).resolve())}}} if a.workdir else {}
    pipe = Pipeline(load_config(None, a.profile, over))
    setup_logging(pipe.ws.logs / f"t2_own_{now_iso().replace(':', '')}.log")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    return run(pipe, a.threads)


if __name__ == "__main__":
    raise SystemExit(main())
