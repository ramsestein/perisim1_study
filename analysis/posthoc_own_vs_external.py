"""Post hoc, EXPLORATORY: adopt, update or build? and a PRAM replica (docs/DECISIONS.md, 2026-11-17, internal
review 7, R3 and R4; `hypo`).

With n local patients a receiving hospital can *adopt* the transported LightGBM (logistic recalibration), *update*
it (LightGBM boosted from the transported model) or build its *own* (LightGBM from scratch), block N's settings.
Within every outer fold and draw: the three options and R4's PRAM arms are fitted on the draw's patients and scored on
the fold's test landmarks; the hospital's own choice comes from a 3-fold patient-grouped cross-validation on its n
patients; the shift diagnostics (calibration slope, expected − observed AUROC) are read on the same n patients.

Usage:  python scripts/posthoc_own_vs_external.py [--units inspire mimic eicu nwicu] [--threads 8]
Outputs (aggregates only): <experiments>/hypo/review/own_vs_external_<unit>.json and reports/own_vs_external.md
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

LOG = logging.getLogger("own_ext")
from own_ext_common import (EXTRA, INNER, N_UPDATE, OPTIONS, GAP_THR, SLOPE_THR, render,  # noqa: E402,F401
                            rule_choice, spearman, summarise)
SIZES = (250, 500, 1000, 2000, 4000)
DRAWS = {250: 5, 500: 5, 1000: 5, 2000: 3, 4000: 3}
ALPHAS = tuple(round(0.1 * i, 1) for i in range(11))
K_PRAM = 50



# =========================================================================== helpers (numpy; tested)
def ll(p, y) -> float:
    return float(RA.PP.ll_rows(np.asarray(p, dtype=np.float64), np.asarray(y, dtype=np.float64)).mean())


def auc(p, y) -> float:
    y = np.asarray(y, dtype=np.float64)
    return RA.PP.wauc(np.asarray(p, dtype=np.float64), y, np.ones_like(y)) if 0 < y.sum() < y.size else float("nan")


def idw_vote(D, I, valid, y_bank, fallback):
    """PRAM's kNN estimate: inverse-distance-weighted mean of the neighbours' outcomes (D squared distances)."""
    d = np.sqrt(np.maximum(D, 0.0))
    w = np.where(valid, 1.0 / (d + 1e-6), 0.0)
    s = w.sum(1)
    v = (w * np.asarray(y_bank, dtype=np.float64)[I]).sum(1)
    return np.where(s > 0, v / np.where(s > 0, s, 1.0), fallback)


def best_alpha(p_base, p_knn, y) -> float:
    return min(ALPHAS, key=lambda a: (ll((1 - a) * p_base + a * p_knn, y), a))


def expected_auroc(p, n_sim: int, seed: int) -> float:
    g = np.random.default_rng(seed)
    v = []
    for _ in range(n_sim):
        ys = (g.random(p.size) < p).astype(np.float64)
        if 0 < ys.sum() < ys.size:
            v.append(auc(p, ys))
    return float(np.mean(v)) if v else float("nan")


def diagnostics(p_tr, y, seed) -> dict:
    """On the hospital's n patients: calibration slope of the transported model and expected − observed AUROC."""
    lp = RA.logit(p_tr)
    _, b = RA.PP._logistic(lp, y, np.ones_like(y), slope=True)
    i0, _ = RA.PP._logistic(lp, y, np.ones_like(y), slope=False)
    obs = auc(p_tr, y)
    exp = expected_auroc(RA.sigmoid(i0 + lp), 20, seed)
    return {"slope": float(b), "auroc_observed": obs, "auroc_expected": exp, "auroc_gap": float(exp - obs)}


# =========================================================================== the unit
def logreg_base(u, units: Path, threads: int) -> np.ndarray:
    """R4: a logistic regression fitted on the development pool as the transported LightGBM was; its predictions."""
    from hypo import compare
    from hypo.frozen import dump, load_pickle
    path = units / f"R4_{'_'.join(sorted(u.dev_sites))}_logreg.pkl"
    if not path.exists():
        cfg, mcfg, space = RA._cfg()
        t = time.perf_counter()
        pred, _ = compare.fit("logreg", RA.dev_pool(u), mcfg, space["baselines"], n_inner=int(cfg["cv"]["inner_folds"]),
                              seed=RA.SEED, threads=threads)
        dump({"pred": pred}, path)
        LOG.info("R4 %s logreg: %.0f s", path.stem, time.perf_counter() - t)
    return np.clip(np.asarray(load_pickle(path)["pred"](u.lm), dtype=np.float64), RA.EPS, 1 - RA.EPS)


def neutral_metric(u, units: Path):
    """R4's distance: the `euclidean` comparator's neutral axes, fitted on (a sample of) the development pool."""
    from perisim.metric.encoding import Encoder
    from hypo.frozen import dump, load_pickle
    from hypo.metric import C, Metric
    path = units / f"R4_{'_'.join(sorted(u.dev_sites))}_neutral.pkl"
    if not path.exists():
        dev = RA.dev_pool(u)
        s = np.random.default_rng(RA.SEED + 71).choice(len(dev), size=min(200000, len(dev)), replace=False)
        sub = dev.take(np.sort(s))
        enc = Encoder(geometry="shape").fit(sub.ft, sub.y, C)
        dump(Metric(enc, np.ones(enc.n_features)), path)
    return load_pickle(path)


def options(Xraw, cat_idx, plg, y, subj, fit, te, seed, threads) -> dict:
    lp = RA.logit(plg)
    return {"adopt": RA.recal("logistic", plg[fit], y[fit], plg[te]),
            "update": RA.lgbm_local(Xraw[fit], y[fit], subj[fit], Xraw[te], cat_idx, seed, threads,
                                    init=lp[fit], init_te=lp[te])[0],
            "own": RA.lgbm_local(Xraw[fit], y[fit], subj[fit], Xraw[te], cat_idx, seed, threads)[0]}


def cv_choice(Xraw, cat_idx, plg, y, subj, fit, seed, threads) -> tuple[str, dict]:
    from sklearn.model_selection import GroupKFold
    L = {a: 0.0 for a in OPTIONS}
    for i, (a_, b_) in enumerate(GroupKFold(INNER).split(fit, groups=subj[fit])):
        P = options(Xraw, cat_idx, plg, y, subj, fit[a_], fit[b_], seed + 31 * (i + 1), threads)
        for a in OPTIONS:
            L[a] += float(RA.PP.ll_rows(P[a], y[fit[b_]]).sum())
    return min(OPTIONS, key=lambda a: L[a]), {a: v / fit.size for a, v in L.items()}


def pram(u, metric, Eb, base, y, fit, te, seed) -> dict:
    """R4: α on 20 % held-out patients (bank = other 80 %), isotonic on their PRAM outputs; bank = all n."""
    from hypo.casebase import CaseBase
    from sklearn.isotonic import IsotonicRegression
    uniq = np.unique(u.subj[fit])
    rng = np.random.default_rng(seed + 5)
    ho = np.isin(u.subj[fit], rng.choice(uniq, size=max(1, int(round(0.2 * uniq.size))), replace=False))
    out, alpha = {}, {}
    cb_in = CaseBase(metric, u.lm.take(fit[~ho]), u.mcfg, E=Eb[fit[~ho]])
    D, I, valid = cb_in.search(Eb[fit[ho]], u.subj[fit[ho]], chunk=20000, k=min(K_PRAM, int(cb_in.uniq.size) - 1))
    cb = CaseBase(metric, u.lm.take(fit), u.mcfg, E=Eb[fit])
    Dt, It, vt = cb.search(Eb[te], u.subj[te], chunk=20000, k=min(K_PRAM, int(cb.uniq.size) - 1))
    for name, p in base.items():
        v_ho = idw_vote(D, I, valid, y[fit[~ho]], p[fit[ho]])
        a = best_alpha(p[fit[ho]], v_ho, y[fit[ho]])
        alpha[name] = a
        mix_ho = (1 - a) * p[fit[ho]] + a * v_ho
        v_te = idw_vote(Dt, It, vt, y[fit], p[te])
        mix = (1 - a) * p[te] + a * v_te
        out[f"pram_{name}"] = np.clip(mix, RA.EPS, 1 - RA.EPS)
        if 0 < y[fit[ho]].sum() < ho.sum():
            iso = IsotonicRegression(y_min=RA.EPS, y_max=1 - RA.EPS, out_of_bounds="clip").fit(mix_ho, y[fit[ho]])
            out[f"pram_{name}_iso"] = np.clip(iso.predict(mix), RA.EPS, 1 - RA.EPS)
        else:
            out[f"pram_{name}_iso"] = out[f"pram_{name}"]
    return out, alpha


def run_unit(u, units: Path, threads: int, with_pram: bool = True) -> dict:
    y = u.y.astype(np.float64)
    plg = u.P["lgbm_transported"]
    Xraw, cat_idx = RA.raw_matrix(u.lm, RA.cat_levels(u.lm))
    p_lr = logreg_base(u, units, threads) if with_pram else None
    metric = neutral_metric(u, units) if with_pram else None
    Eb = metric.embed(u.lm) if with_pram else None
    n_pat_min = min(np.unique(u.subj[u.split(f)[0]]).size for f in u.folds)
    sizes = [n for n in SIZES if n < n_pat_min]
    cache = units / "own_vs_external"
    cache.mkdir(exist_ok=True)
    samples = []
    for n in sizes:
        for r in range(DRAWS[n]):
            for f in u.folds:
                path = cache / f"{u.name}_n{n}_r{r}_f{f}.json"
                if path.exists():
                    samples.append(json.loads(path.read_text(encoding="utf-8")))
                    continue
                t0 = time.perf_counter()
                tr, te = u.split(f)
                fit = tr[u.draw(f, tr, int(n), r)]
                seed = u.seed + 100 * f + 17 * r + n
                P = options(Xraw, cat_idx, plg, y, u.subj, fit, te, seed, threads)
                P["adopt_isotonic"] = RA.recal("isotonic", plg[fit], y[fit], plg[te])
                P["lgbm_base"] = plg[te]
                alpha = {}
                if with_pram:
                    P["lr_base"] = p_lr[te]
                    P["lr_logistic"] = RA.recal("logistic", p_lr[fit], y[fit], p_lr[te])
                    Q, alpha = pram(u, metric, Eb, {"lgbm": plg, "lr": p_lr}, y, fit, te, seed)
                    P.update(Q)
                ch, cvl = cv_choice(Xraw, cat_idx, plg, y, u.subj, fit, seed, threads)
                dg = diagnostics(plg[fit], y[fit], seed + 3)
                rec = {"n": n, "r": r, "f": int(f), "events_fit": int(y[fit].sum()), "test_rows": int(te.size),
                       "ll": {a: ll(p, y[te]) for a, p in P.items()}, "auc": {a: auc(p, y[te]) for a, p in P.items()},
                       "cv_choice": ch, "cv_logloss": cvl, "diag": dg, "rule_choice": rule_choice(dg, n),
                       "alpha": alpha, "seconds": time.perf_counter() - t0}
                path.write_text(json.dumps(rec), encoding="utf-8")
                samples.append(rec)
                LOG.info("own/ext %s n=%d r=%d f%d: cv→%s (%.0f s)", u.name, n, r, f, ch, rec["seconds"])
    out = summarise(samples, sizes)
    out.update({"unit": u.name, "sizes": sizes, "draws": {str(n): DRAWS[n] for n in sizes},
                "rule": {"slope_below": SLOPE_THR, "auroc_gap_above": GAP_THR, "update_from_n": N_UPDATE}})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--units", nargs="*", default=list(RA.ROTATIONS) + ["nwicu"])
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--no-pram", action="store_true")
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
            res[u.name] = run_unit(u, units, a.threads, with_pram=not a.no_pram)
            (od / f"own_vs_external_{X}.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
        LOG.info("own/ext %s done", X)
    allres = {}
    for f in sorted(od.glob("own_vs_external_*.json")):
        allres.update(json.loads(f.read_text(encoding="utf-8")))
    rep = external_dir().parent / "reports" / "own_vs_external.md"
    rep.write_text(render(allres), encoding="utf-8")
    LOG.info("own/ext: %s", rep)
    check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
