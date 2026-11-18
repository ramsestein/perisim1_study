"""Post hoc, EXPLORATORY: a semi-synthetic map of when the update answer changes (docs/DECISIONS.md, 2026-11-16,
internal review 6, R1).

In each rotation destination the "truth" p0 is block N's out-of-fold LightGBM refitted on all local labels. Synthetic
risks logit p* = logit p0 + η·q + γ·s, with s the standardised part of the transported no-MAP LightGBM's logit that is
orthogonal to the transported LightGBM's logit (a relation shift: risk the transported score does not carry) and q the
standardised square of the centred logit of p0 (a non-monotone change of the link). Training labels y* ~ Bernoulli(p*);
the test fold is scored against p* (expected log-loss and its excess over p*), so no label noise enters the reading.

Usage:  python scripts/posthoc_shift_map.py [--units inspire mimic eicu] [--threads 8]
Outputs (aggregates only): <experiments>/hypo/review/shift_map_<unit>.json and reports/shift_map_<unit>.md
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
import review_analyses as RA  # noqa: E402

LOG = logging.getLogger("shift_map")
ETAS = (0.0, 0.3)
GAMMAS = (0.0, 0.25, 0.5, 1.0)
SIZES = (250, 1000, 4000, "all")
DRAWS = {250: 3, 1000: 3, 4000: 2, "all": 1}
ARMS = ("intercept", "logistic", "isotonic", "scratch", "warm", "knn_1d", "knn_nca", "stack")


def scenarios():
    return [(e, g) for e in ETAS for g in GAMMAS]


def orth_std(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """The standardised residual of a regressed (OLS, with intercept) on b."""
    A = np.column_stack([np.ones_like(b), b])
    r = a - A @ np.linalg.lstsq(A, a, rcond=None)[0]
    return (r - r.mean()) / r.std()


def sq_std(x: np.ndarray) -> np.ndarray:
    c = (x - x.mean()) ** 2
    return (c - c.mean()) / c.std()


def excess_logloss(q: np.ndarray, p: np.ndarray) -> float:
    """Expected log-loss of q under outcomes drawn from p, minus that of p itself (= mean KL(p || q))."""
    q = np.clip(q, RA.EPS, 1 - RA.EPS)
    p = np.clip(p, RA.EPS, 1 - RA.EPS)
    return float(np.mean(p * np.log(p / q) + (1 - p) * np.log((1 - p) / (1 - q))))


def chosen_k(od: Path, uname: str, arm: str) -> tuple[int, float]:
    """The modal k (and its α) block N chose for an arm in this unit (review_N_*.json or review.json)."""
    for f in sorted(od.glob("review_N_*.json")) + [od / "review.json"]:
        if not f.exists():
            continue
        r = json.loads(f.read_text(encoding="utf-8")).get("N", {})
        if uname in r:
            ch = r[uname]["N1"]["chosen"][arm]
            ks = [c["k"] for c in ch]
            k = max(set(ks), key=ks.count)
            a = [c["alpha"] for c in ch if c["k"] == k][0]
            return int(k), float(a)
    return int(RA._cfg()[1]["k"]), 1.0


def neighbours(u, metric, E, fit, te, k, sample, seed):
    """One search per (fold, size, draw): the test rows' neighbours and those of a sample of the training rows (own
    patient excluded), reused for every scenario's labels."""
    from hypo.casebase import CaseBase
    cb = CaseBase(metric, u.lm.take(fit), u.mcfg, E=E[fit])
    k = min(k, int(cb.uniq.size) - 1)
    _, I, valid = cb.search(E[te], u.subj[te], chunk=5000, k=k)
    s = np.random.default_rng(seed).choice(fit.size, size=min(sample, fit.size), replace=False)
    _, Is, vs = cb.search(cb.E[s], cb.subj_s[s], chunk=5000, k=k)
    return cb, k, (I, valid), (s, Is, vs)


def vote(cb, k, alpha, I, valid, labels, prior=None):
    lab = np.asarray(labels, dtype=np.int64)
    if prior is None:
        prior = np.bincount(lab, minlength=2) / max(lab.size, 1)
    return cb.probs(I, valid, k, alpha=alpha, labels=lab, prior=prior)[:, 1]


def run_unit(u, units: Path, od: Path, threads: int) -> dict:
    from sklearn.linear_model import LogisticRegression
    import warnings

    n_rows = len(u.lm)
    share_key = u.name
    p0 = np.full(n_rows, np.nan)
    for f in u.folds:
        _, te = u.split(f)
        p0[te] = np.load(units / f"N_scratch_{share_key}_f{f}.npz")["p"]
    plg = u.P["lgbm_transported"]
    pn = RA.submodel_p(u, units, "nomap", threads)
    s = orth_std(RA.logit(pn), RA.logit(plg))
    q = sq_std(RA.logit(p0))
    SC = scenarios()
    pstar = {sc: RA.sigmoid(RA.logit(p0) + sc[0] * q + sc[1] * s) for sc in SC}
    ystar = {sc: (np.random.default_rng([RA.SEED, 61, i, u.ci]).random(n_rows) < pstar[sc]).astype(np.int64)
             for i, sc in enumerate(SC)}
    Xraw, cat_idx = RA.raw_matrix(u.lm, RA.cat_levels(u.lm))
    E1 = RA.logit(plg)[:, None].astype(np.float32)
    k1, a1 = chosen_k(od, u.name, "knn_1d_tuned")
    k2, a2 = chosen_k(od, u.name, "perisim_tuned")
    n_pat_min = min(np.unique(u.subj[u.split(f)[0]]).size for f in u.folds)
    sizes = [n for n in SIZES if n == "all" or n < n_pat_min]
    cache = units / "shift_map"
    cache.mkdir(exist_ok=True)
    res = {}                                   # (eta, gamma, n) -> arm -> list over draws of the pooled excess
    for n in sizes:
        for r in range(DRAWS[n]):
            path = cache / f"{u.name}_n{n}_r{r}.json"
            if path.exists():
                cell = json.loads(path.read_text(encoding="utf-8"))
            else:
                t0 = time.perf_counter()
                acc = {f"{sc[0]}|{sc[1]}": {a: 0.0 for a in ARMS} for sc in SC}
                tot = 0
                for f in u.folds:
                    tr, te = u.split(f)
                    fit = tr if n == "all" else tr[u.draw(f, tr, int(n), r)]
                    seed = u.seed + 100 * f + 13 * r
                    cbN, kN, (IN, vN), (sN, IsN, vsN) = neighbours(u, u.metric, u.E, fit, te, k2, 20000, seed)
                    cb1, kk1, (I1, v1), _ = neighbours(u, RA._Score(), E1, fit, te, k1, 10, seed)
                    for sc in SC:
                        y = ystar[sc]
                        P = {m: RA.recal(m, plg[fit], y[fit], plg[te]) for m in ("intercept", "logistic", "isotonic")}
                        P["scratch"], _ = RA.lgbm_local(Xraw[fit], y[fit], u.subj[fit], Xraw[te], cat_idx, seed, threads)
                        P["warm"], _ = RA.lgbm_local(Xraw[fit], y[fit], u.subj[fit], Xraw[te], cat_idx, seed, threads,
                                                     init=RA.logit(plg[fit]), init_te=RA.logit(plg[te]))
                        P["knn_1d"] = vote(cb1, kk1, a1, I1, v1, y[fit])
                        P["knn_nca"] = vote(cbN, kN, a2, IN, vN, y[fit])
                        v_tr = vote(cbN, kN, a2, IsN, vsN, y[fit], prior=cbN.loo_prior(labels=y[fit])[sN])
                        Z = np.column_stack([RA.logit(plg[fit][sN]), RA.logit(v_tr)])
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            m = LogisticRegression(C=1e4, max_iter=3000).fit(Z, y[fit][sN]) if \
                                0 < y[fit][sN].sum() < sN.size else None
                        P["stack"] = m.predict_proba(np.column_stack([RA.logit(plg[te]), RA.logit(P["knn_nca"])]))[:, 1] \
                            if m is not None else P["logistic"]
                        key = f"{sc[0]}|{sc[1]}"
                        for a in ARMS:
                            acc[key][a] += excess_logloss(P[a], pstar[sc][te]) * te.size
                    tot += te.size
                cell = {k: {a: v / tot for a, v in d.items()} for k, d in acc.items()}
                cell["_seconds"] = time.perf_counter() - t0
                path.write_text(json.dumps(cell), encoding="utf-8")
                LOG.info("shift map %s n=%s r=%d: %.0f s", u.name, n, r, cell["_seconds"])
            for key, d in cell.items():
                if key.startswith("_"):
                    continue
                for a, v in d.items():
                    res.setdefault(f"{key}|{n}", {}).setdefault(a, []).append(v)
    table = {}
    for key, d in res.items():
        eta, gam, n = key.split("|")
        row = {a: {"mean": float(np.mean(v)), "min": float(np.min(v)), "max": float(np.max(v))} for a, v in d.items()}
        best = min(row, key=lambda a: row[a]["mean"])
        table[key] = {"eta": float(eta), "gamma": float(gam), "n": n, "arms": row, "best": best}
    reading = {}
    for eta in ETAS:
        for n in sizes:
            gs = [g for g in GAMMAS if f"{eta}|{g}|{n}" in table and
                  min(table[f"{eta}|{g}|{n}"]["arms"][a]["mean"] for a in ("scratch", "warm")) <
                  table[f"{eta}|{g}|{n}"]["arms"]["logistic"]["mean"]]
            reading[f"{eta}|{n}"] = {"smallest_gamma_reestimation_beats_logistic": gs[0] if gs else None}
    sim_best = [k for k, v in table.items() if v["best"] in ("knn_nca", "stack", "knn_1d")]
    return {"unit": u.name, "k": {"knn_1d": k1, "knn_nca": k2}, "sd_s": 1.0,
            "mean_p0": float(np.mean(p0)), "mean_pstar": {f"{e}|{g}": float(np.mean(pstar[(e, g)])) for e, g in SC},
            "table": table, "reading": reading, "similarity_best_in": sim_best}


def render(r: dict) -> str:
    L = [f"# Semi-synthetic shift map — {r['unit']} (post hoc, exploratory)", "",
         f"k: kNN-1D {r['k']['knn_1d']}, kNN-NCA {r['k']['knn_nca']}. Cells: excess expected log-loss over the true "
         "risk (nats, mean over draws); best arm in bold.", "",
         "| η | γ | n | " + " | ".join(ARMS) + " |", "|---|---|---|" + "---|" * len(ARMS)]
    for key, v in sorted(r["table"].items(), key=lambda t: (t[1]["eta"], t[1]["gamma"], str(t[1]["n"]))):
        cells = [(f"**{v['arms'][a]['mean']:.4f}**" if a == v["best"] else f"{v['arms'][a]['mean']:.4f}") for a in ARMS]
        L.append(f"| {v['eta']} | {v['gamma']} | {v['n']} | " + " | ".join(cells) + " |")
    L += ["", "Smallest γ at which re-estimation beats the logistic recalibration: " +
          "; ".join(f"η={k.split('|')[0]}, n={k.split('|')[1]}: {v['smallest_gamma_reestimation_beats_logistic']}"
                    for k, v in r["reading"].items()),
          "", f"Similarity arm best in: {', '.join(r['similarity_best_in']) or 'none'}"]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--units", nargs="*", default=list(RA.ROTATIONS))
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
    for X in a.units:
        u = RA.unit_hypo(st, X)
        r = run_unit(u, units, od, a.threads)
        (od / f"shift_map_{X}.json").write_text(json.dumps(r, indent=1), encoding="utf-8")
        rep = external_dir().parent / "reports" / f"shift_map_{X}.md"
        rep.write_text(render(r), encoding="utf-8")
        LOG.info("shift map %s: %s", X, rep)
    check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
