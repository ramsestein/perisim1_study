"""Post hoc, EXPLORATORY: the vasopressor stratum in every `hypo` unit (docs/DECISIONS.md, 2026-11-17, internal
review 8, R8).

With all local labels: in landmarks with and without a vasopressor running, calibration in the large and slope of the
transported LightGBM after logistic recalibration fitted on all strata (fold by fold), and the log-loss differences
recalibrated − own (block N's scratch refit) and recalibrated − update (block N's boosted refit), with patient-bootstrap
95 % CIs (1,000).

Usage:  python scripts/posthoc_vaso_strata.py [--units inspire mimic eicu nwicu]
Outputs (aggregates only): <experiments>/hypo/review/vaso_strata.json and reports/vaso_strata.md
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_analyses as RA  # noqa: E402

LOG = logging.getLogger("vaso")
N_BOOT = 1000


def stratum_stats(p_rec, p_own, p_upd, y, subj, seed) -> dict:
    lr, lo, lu = (RA.PP.ll_rows(p, y) for p in (p_rec, p_own, p_upd))
    x = RA.logit(p_rec)
    one = np.ones_like(y)
    citl, _ = RA.PP._logistic(x, y, one, slope=False)
    _, slope = RA.PP._logistic(x, y, one, slope=True)
    B = {"citl": [], "slope": [], "rec_minus_own": [], "rec_minus_update": []}
    for w in RA.PP.boot_weights(subj, N_BOOT, seed):
        sw = w.sum()
        B["rec_minus_own"].append(float(w @ (lr - lo)) / sw)
        B["rec_minus_update"].append(float(w @ (lr - lu)) / sw)
        B["citl"].append(RA.PP._logistic(x, y, w, slope=False)[0])
        B["slope"].append(RA.PP._logistic(x, y, w, slope=True)[1])
    est = {"citl": float(citl), "slope": float(slope), "rec_minus_own": float((lr - lo).mean()),
           "rec_minus_update": float((lr - lu).mean())}
    return {k: {"est": est[k], "ci95": RA.PP.ci(B[k])} for k in est} | {
        "landmarks": int(y.size), "patients": int(np.unique(subj).size), "prevalence": float(y.mean())}


def run_unit(u, units: Path) -> dict:
    y = u.y.astype(np.float64)
    plg = u.P["lgbm_transported"]
    share_key = "nwicu" if u.name.startswith("nwicu") else u.name
    rec, own, upd = (np.full(y.size, np.nan) for _ in range(3))
    for f in u.folds:
        tr, te = u.split(f)
        rec[te] = RA.recal("logistic", plg[tr], y[tr], plg[te])
        own[te] = np.load(units / f"N_scratch_{share_key}_f{f}.npz")["p"]
        upd[te] = np.load(units / f"N_{u.name}_f{f}.npz", allow_pickle=True)["warm_all"]
    S = RA.strata(u)
    out = {}
    for name in ("vaso_on=0", "vaso_on=1"):
        s = S.get(name)
        if s is None or np.unique(u.subj[s]).size < 100 or y[s].sum() < 10:
            out[name] = {"skipped": "fewer than 100 patients or 10 events"}
            continue
        out[name] = stratum_stats(rec[s], own[s], upd[s], y[s], u.subj[s], RA.SEED + 201)
    v1 = out.get("vaso_on=1", {})
    v0 = out.get("vaso_on=0", {})
    rep = None
    if "citl" in v1:
        lo, hi = v1["citl"]["ci95"]
        beyond = lo > 0.10 or hi < -0.10
        gap = v1["rec_minus_own"]["ci95"][0] > v0["rec_minus_own"]["ci95"][1]
        rep = bool(beyond or gap)
    out["replicates"] = rep
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--units", nargs="*", default=list(RA.ROTATIONS) + ["nwicu"])
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
                        stream=sys.stdout)
    from hypo.external import Stage
    from hypo.frozen import check, external_dir

    RA.QUICK = a.quick
    check()
    st = Stage(quick=a.quick, threads=4)
    od = external_dir().with_name("review")
    units = od / "units"
    res, cache = {}, {}
    for X in a.units:
        for u in ([RA.unit_nwicu(st, e, cache) for e in RA.ROTATIONS] if X == "nwicu" else [RA.unit_hypo(st, X)]):
            res[u.name] = run_unit(u, units)
            LOG.info("vaso %s: replicates=%s", u.name, res[u.name]["replicates"])
    (od / "vaso_strata.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    L = ["# Vasopressor stratum in every unit (post hoc, exploratory; internal review 8, R8)", "",
         "Transported LightGBM after logistic recalibration on all local labels. CITL and slope within the stratum; "
         "Δ log-loss recalibrated − own and recalibrated − update (nats; 95 % patient-bootstrap CI).", "",
         "| unit | stratum | patients | prevalence | CITL | slope | recal − own | recal − update |", "|---|---|---|---|---|---|---|---|"]
    f = lambda d: f"{d['est']:+.3f} ({d['ci95'][0]:+.3f} to {d['ci95'][1]:+.3f})"
    g = lambda d: f"{d['est']:+.4f} ({d['ci95'][0]:+.4f} to {d['ci95'][1]:+.4f})"
    for un, r in res.items():
        for s in ("vaso_on=0", "vaso_on=1"):
            d = r[s]
            if "skipped" in d:
                L.append(f"| {un} | {s} | — | — | {d['skipped']} | | | |")
                continue
            L.append(f"| {un} | {s} | {d['patients']:,} | {d['prevalence']:.3f} | {f(d['citl'])} | {f(d['slope'])} | "
                     f"{g(d['rec_minus_own'])} | {g(d['rec_minus_update'])} |")
        L.append(f"| {un} | replicates (rule fixed in DECISIONS) | {r['replicates']} | | | | | |")
    rep = external_dir().parent / "reports" / "vaso_strata.md"
    rep.write_text("\n".join(L) + "\n", encoding="utf-8")
    LOG.info("vaso: %s", rep)
    check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
