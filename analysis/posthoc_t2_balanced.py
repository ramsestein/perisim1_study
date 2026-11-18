"""Post hoc, EXPLORATORY: T2 with balanced options (docs/DECISIONS.md, 2026-11-19, internal review 9).

The same draws, transported model and test set as posthoc_t2_own.py (R2's draws of n local pool patients in MIMIC-IV
and eICU; development INSPIRE). Options balanced as in phase 2: *update* (multiclass LightGBM boosted from the
transported model) and *build* (multiclass LightGBM from scratch) choose their number of boosting iterations by a
3-fold patient-grouped cross-validation on the n patients and are refitted on all n; *adopt* is the multinomial
recalibration of offsets + common slope. Fixed settings otherwise (31 leaves, ≥ 50 per leaf, rate 0.05).

Usage:  python scripts/posthoc_t2_balanced.py [--threads 4]
Outputs (aggregates only): <workdir>/experiments/t2/results/posthoc/t2_balanced.json and reports/t2_balanced.md
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
import posthoc_t2_ladder as LD  # noqa: E402  (sets the frozen src on sys.path)

PT = LD.PT
LOG = logging.getLogger("t2_bal")
SIZES = (250, 500, 1000, 2000, 4000, 8000)
INNER, MAX_IT, PATIENCE = 3, 2000, 50


def _params(C, seed, threads):
    return {"objective": "multiclass", "num_class": C, "learning_rate": 0.05, "num_leaves": 31,
            "min_data_in_leaf": 50, "bagging_fraction": 0.8, "bagging_freq": 1, "feature_fraction": 0.8,
            "deterministic": True, "force_col_wise": True, "num_threads": threads, "seed": seed, "verbose": -1}


def lgbm_multi_balanced(X, y, subj, X_te, C, seed, threads, init=None, init_te=None):
    import lightgbm as lgb
    from sklearn.model_selection import GroupKFold
    base = 0.0 if init_te is None else init_te
    if np.unique(y).size < 2:
        prior = np.bincount(y, minlength=C) / len(y)
        return np.tile(prior, (X_te.shape[0], 1)) if init_te is None else LD.softmax(init_te), 0
    ini = (lambda m: None) if init is None else (lambda m: init[m].ravel(order="F"))
    its = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for a, b in GroupKFold(INNER).split(X, groups=subj):
            if np.unique(y[a]).size < 2:
                continue
            dtr = lgb.Dataset(X[a], y[a], init_score=ini(a), free_raw_data=False)
            dva = lgb.Dataset(X[b], y[b], init_score=ini(b), reference=dtr)
            m = lgb.train(_params(C, seed, threads), dtr, MAX_IT, valid_sets=[dva],
                          callbacks=[lgb.early_stopping(PATIENCE, verbose=False)])
            its.append(int(m.best_iteration or m.current_iteration()))
        it = int(round(np.mean(its))) if its else 50
        all_ = np.arange(len(y))
        m = lgb.train(_params(C, seed, threads), lgb.Dataset(X, y, init_score=ini(all_)), max(it, 1))
    raw = m.predict(X_te, raw_score=True)
    return LD.softmax(base + raw.reshape(X_te.shape[0], C)), it


def run(pipe, threads: int) -> int:
    cfg, ws = pipe.cfg, pipe.ws
    t = "t2"
    externals = [c for c in cfg.experiment["cohorts"]["external"] if c in pipe.available_cohorts()]
    args = {"names": pipe.feature_names(), "dev": cfg.experiment["cohorts"]["development"], "externals": externals,
            "threads": threads}
    lcache = ws.predictions("posthoc", t) / "ladder"
    cache = ws.predictions("posthoc", t) / "balanced"
    cache.mkdir(parents=True, exist_ok=True)
    fm = PT._load(ws.predictions("external", t) / "final_model.pkl")
    enc = fm["enc"]
    ins = None
    out = {"note": "Exploratory, post hoc (internal review 9, 2026-11-19): balanced update and build.", "cohorts": {}}
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
                a_, b_ = PT.fit_recal(P_all[fit], y[fit], slope=True)
                Lf, Lq = np.log(np.clip(P_all[fit], LD.EPS, 1)), np.log(np.clip(P_all[q], LD.EPS, 1))
                Pu, itu = lgbm_multi_balanced(Xm[fit], y[fit], sX[fit], Xm[q], C, seed, threads, init=Lf, init_te=Lq)
                Pb, itb = lgbm_multi_balanced(Xm[fit], y[fit], sX[fit], Xm[q], C, seed, threads)
                P = {"adopt": PT.apply_recal(P_all[q], a_, b_), "update": Pu, "build": Pb}
                rec = {"n": n, "r": r, "ll": {o: LD.logloss(p, y[q]) for o, p in P.items()},
                       "iterations": {"update": itu, "build": itb}, "seconds": time.perf_counter() - t0}
                path.write_text(json.dumps(rec), encoding="utf-8")
                samples.append(rec)
                LOG.info("t2 balanced %s n=%d r=%d: adopt %.4f update %.4f build %.4f (%.0f s)", c, n, r,
                         rec["ll"]["adopt"], rec["ll"]["update"], rec["ll"]["build"], rec["seconds"])
        res = {"sizes": sizes, "test_rows": int(q.size), "pool_patients": int(pats.size), "by_n": {}}
        for n in sizes:
            S = [s for s in samples if s["n"] == n]
            o = {"samples": len(S), "logloss_mean": {k: float(np.mean([s["ll"][k] for s in S])) for k in S[0]["ll"]}}
            for a, b in (("build", "update"), ("build", "adopt"), ("update", "adopt")):
                d = np.array([s["ll"][a] - s["ll"][b] for s in S])
                o[f"{a}_vs_{b}"] = {"mean": float(d.mean()), "share_wins": float((d < 0).mean())}
            res["by_n"][str(n)] = o
        res["breakeven_80pct"] = {k: next((n for n in sizes if res["by_n"][str(n)][k]["share_wins"] >= 0.8), None)
                                  for k in ("build_vs_update", "build_vs_adopt", "update_vs_adopt")}
        out["cohorts"][c] = res
    rd = ws.root / "results" / "posthoc"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "t2_balanced.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    L = ["# T2 with balanced options (exploratory)", "", "| cohort | n | adopt | update | build | build − update (share) |",
         "|---|---|---|---|---|---|"]
    for c, r in out["cohorts"].items():
        for n, o in r["by_n"].items():
            lm, d = o["logloss_mean"], o["build_vs_update"]
            L.append(f"| {c} | {n} | {lm['adopt']:.4f} | {lm['update']:.4f} | {lm['build']:.4f} | "
                     f"{d['mean']:+.4f} ({d['share_wins']:.2f}) |")
    (ws.reports / "t2_balanced.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    LOG.info("t2 balanced: %s", rd / "t2_balanced.json")
    return 0


def main(argv=None) -> int:
    from perisim.config import load_config
    from perisim.pipeline import Pipeline
    from perisim.utils import now_iso, setup_logging

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--profile", default=None)
    ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args(argv)
    pipe = Pipeline(load_config(None, a.profile, {}))
    setup_logging(pipe.ws.logs / f"t2_balanced_{now_iso().replace(':', '')}.log")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    return run(pipe, a.threads)


if __name__ == "__main__":
    raise SystemExit(main())
