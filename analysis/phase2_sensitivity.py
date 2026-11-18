"""Phase 2 sensitivity analyses (EXPLORATORY, not registered; docs/DECISIONS.md, 2026-11-19, internal review 9).

Two analyses asked for by the internal review of the manuscript, written before they run:

--margin   Re-reads the cached phase 2 samples (units/phase2/*.json; no model is refitted) and counts a win only when
           the loss difference exceeds a margin m in {0, 0.001, 0.002} nats: build vs update, best own vs best
           external, and the G2 estimator (risk difference flagged − unflagged, unit-clustered bootstrap) by scenario.
--set N    The NWICU units of the first part (hypotension from each rotation model, O1, O2 from each pair of systems)
           re-run with phase 2's balanced options and no induced error, at 250, 500 and 1,000 patients (2 draws
           within each of the 5 folds), so that NWICU joins the 8 rotation units (set M, level M0).

Usage:  python scripts/phase2_sensitivity.py --margin
        python scripts/phase2_sensitivity.py --set N [--threads 5]
Outputs (aggregates only): <experiments>/hypo/review/phase2_margin.json, phase2_N.json, reports/phase2_sensitivity.md
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import phase2_realism as P2  # noqa: E402

LOG = logging.getLogger("phase2_sens")
MARGINS = (0.0, 0.001, 0.002)
P2.SIZES["N"] = (250, 500, 1000)
P2.DRAWS["N"] = {250: 2, 500: 2, 1000: 2}
ROT = ("inspire", "mimic", "eicu")
O_NW = {"O1": [("mimic", "eicu")], "O2": [("mimic", "eicu"), ("inspire", "eicu"), ("inspire", "mimic")]}
NAME = re.compile(r"^(?P<unit>.+)_n(?P<n>\d+)_r(?P<r>\d+)_f(?P<f>\d+)\.json$")


def scenario(unit: str) -> str | None:
    if unit.startswith("H_"):
        return "H"
    if unit.startswith("T_"):
        return "T"
    if unit.startswith("M_"):
        return "M0" if unit.endswith("_M0") else "M1-M3"
    if unit.startswith("N_"):
        return "N"
    return None


def margin(cache: Path) -> dict:
    by_unit: dict[str, list] = {}
    for p in sorted(cache.glob("*.json")):
        m = NAME.match(p.name)
        if not m:
            continue
        s = json.loads(p.read_text(encoding="utf-8"))
        s["n"] = int(m["n"])
        by_unit.setdefault(m["unit"], []).append(s)
    out = {"margins": list(MARGINS), "units": {}, "scenarios": {}}
    for u, S in by_unit.items():
        rec = {"scenario": scenario(u), "by_n": {}}
        for n in sorted({s["n"] for s in S}):
            T = [s for s in S if s["n"] == n]
            bu = np.array([s["ll"]["build"] - s["ll"]["update"] for s in T])
            oe = np.array([s["ll"][s["best_own"]] - s["ll"][s["best_ext"]] for s in T])
            rec["by_n"][str(n)] = {"samples": len(T), **{
                f"m{m_}": {"build_beats_update": float((bu < -m_).mean()), "update_beats_build": float((bu > m_).mean()),
                           "own_beats_ext": float((oe < -m_).mean()), "ext_beats_own": float((oe > m_).mean())}
                for m_ in MARGINS}}
        out["units"][u] = rec
    groups = {"H": ["H"], "T": ["T"], "M0": ["M0"], "M1-M3": ["M1-M3"], "H+T+M0": ["H", "T", "M0"],
              "H+T+M (registered pool)": ["H", "T", "M0", "M1-M3"]}
    for g, members in groups.items():
        units = [u for u in by_unit if scenario(u) in members]
        if not units:
            continue
        out["scenarios"][g] = {}
        for m_ in MARGINS:
            pairs = {u: [[bool(s["flag"]), bool(s["ll"][s["best_own"]] < s["ll"][s["best_ext"]] - m_)]
                         for s in by_unit[u]] for u in units}
            r = P2.risk_difference_ci(pairs)
            out["scenarios"][g][f"m{m_}"] = {"units": len(units), **r}
    return out


def units_N(st, sy, cache, threads, seed):
    from hypo.frozen import final_dir, load_pickle
    import phase1_new_outcomes as P1
    k = 0
    lm, fold = sy.full("nwicu")
    for e in ROT:
        model = load_pickle(final_dir() / f"comp_ext-{e}_lightgbm.pkl")
        plg = np.clip(np.asarray(model(lm), dtype=np.float64), P2.RA.EPS, 1 - P2.RA.EPS)
        k += 1
        yield P2.Unit2(f"N_hypo_nwicu_{e}", "N", "hypo", lm, plg, seed, 300 + k, fold=fold)
    for outcome, plans in O_NW.items():
        lo, fo = sy.outcome("nwicu", outcome)
        for src in plans:
            try:
                model = P1.external_model(sy, outcome, src, cache, threads)
            except RuntimeError as err:
                LOG.warning("%s", err)
                continue
            plg = np.clip(np.asarray(model(lo), dtype=np.float64), P2.RA.EPS, 1 - P2.RA.EPS)
            k += 1
            yield P2.Unit2(f"N_{outcome}_nwicu_{'+'.join(src)}", "N", outcome, lo, plg, seed, 300 + k, fold=fo)


def render(mg: dict | None, nres: dict | None) -> str:
    L = ["# Phase 2 sensitivity analyses (exploratory, internal review 9)", ""]
    if mg:
        L += ["## Wins with a minimum margin", "", "Risk difference of 'best own beats best external by more than m' "
              "between flagged and unflagged samples (unit-clustered bootstrap 95 % CI).", "",
              "| scenario | units | m | risk difference (95 % CI) | own wins | PPV | NPV |", "|---|---|---|---|---|---|---|"]
        for g, d in mg["scenarios"].items():
            for k, r in d.items():
                e, c = r["estimate"], r["ci95"]["rd"]
                L.append(f"| {g} | {r['units']} | {k[1:]} | {e['rd']:.3f} ({c[0]:.3f} to {c[1]:.3f}) | "
                         f"{e['own_wins'] / max(e['samples'], 1):.3f} | {e['ppv']:.2f} | {e['npv']:.2f} |")
        L.append("")
    if nres:
        L += ["## NWICU with balanced options (set N)", "", "| unit | n | build − update (share build wins) | "
              "update − adopt (share) | best own − best ext (share) |", "|---|---|---|---|---|"]
        for u, r in nres.items():
            for n, o in r.get("by_n", {}).items():
                a, b, c = o["build_vs_update"], o["update_vs_adopt"], o["best_own_vs_best_ext"]
                L.append(f"| {u} | {n} | {a['mean']:+.4f} ({a['share_wins']:.2f}) | {b['mean']:+.4f} ({b['share_wins']:.2f}) "
                         f"| {c['mean']:+.4f} ({c['share_wins']:.2f}) |")
        L.append("")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--margin", action="store_true")
    ap.add_argument("--set", choices=["N"], default=None)
    ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
                        stream=sys.stdout)
    from hypo.frozen import check, external_dir
    od = external_dir().with_name("review")
    cache = od / "units" / "phase2"
    ext_cache = od / "units" / "phase1"
    mg = nres = None
    if a.set == "N":
        from hypo.external import Stage
        import phase1_new_outcomes as P1
        P2.RA.PP._logistic = P2.C.logistic_guarded
        check()
        st = Stage(quick=False, threads=a.threads)
        sy = P1.Systems(st)
        cfg, _, _ = P2.RA._cfg()
        seed = int(cfg["seed"])
        out_file = od / "phase2_N.json"
        nres = json.loads(out_file.read_text(encoding="utf-8")) if out_file.exists() else {}
        for u in units_N(st, sy, ext_cache, a.threads, seed):
            try:
                nres[u.name] = P2.run_unit(u, cache, a.threads)
            except Exception as e:
                LOG.exception("unit %s failed", u.name)
                nres[u.name] = {"dropped": f"{type(e).__name__}: {e}", "set": "N"}
            out_file.write_text(json.dumps(nres, indent=1, default=float), encoding="utf-8")
            LOG.info("phase2 N %s done", u.name)
        check()
    if a.margin:
        mg = margin(cache)
        (od / "phase2_margin.json").write_text(json.dumps(mg, indent=1, default=float), encoding="utf-8")
    pm, pn = od / "phase2_margin.json", od / "phase2_N.json"
    mg = mg or (json.loads(pm.read_text(encoding="utf-8")) if pm.exists() else None)
    nres = nres or (json.loads(pn.read_text(encoding="utf-8")) if pn.exists() else None)
    rep = external_dir().parent / "reports" / "phase2_sensitivity.md"
    rep.write_text(render(mg, nres), encoding="utf-8")
    LOG.info("phase2 sensitivity: %s", rep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
