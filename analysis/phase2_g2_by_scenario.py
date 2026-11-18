"""Phase 2, exploratory (not a registered analysis): accuracy of the per-sample shift diagnosis by scenario.

Same estimator as the registered G2 (risk difference of "best own beats best external" between flagged and
unflagged samples, bootstrap clustered by unit, 2,000 replicates, seed 0), computed within each scenario from the
per-sample (flag, own_beats_ext) pairs stored in the phase 2 aggregates. Needs only numpy; run from the repository
root:  python analysis/phase2_g2_by_scenario.py
Output: results/confirmatory_phase2/exploratory_g2_by_scenario.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results" / "confirmatory_phase2"


def risk_difference_ci(pairs_by_unit: dict, n_boot: int = 2000, seed: int = 0) -> dict:
    """Copied from analysis/phase2_realism.py (the registered G2 estimator)."""
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


def main() -> None:
    units = {}
    for f in sorted(RES.glob("phase2_*.json")):
        if f.name in ("phase2_hypotheses.json", "phase2_H_O2_units.json"):
            continue
        for k, u in json.loads(f.read_text(encoding="utf-8")).items():
            if isinstance(u, dict) and "set" in u:
                units[k] = u
    pairs = {k: u["pairs"] for k, u in units.items()}
    groups = {
        "H": [k for k, u in units.items() if u["set"] == "H"],
        "T": [k for k, u in units.items() if u["set"] == "T"],
        "M0": [k for k, u in units.items() if u["set"] == "M" and k.endswith("_M0")],
        "M1-M3": [k for k, u in units.items() if u["set"] == "M" and not k.endswith("_M0")],
    }
    groups["H+T+M0"] = groups["H"] + groups["T"] + groups["M0"]
    out = {}
    for g, ks in groups.items():
        r = risk_difference_ci({k: pairs[k] for k in ks})
        out[g] = {"units": len(ks), "samples": r["estimate"]["samples"], "flagged": r["estimate"]["flagged"],
                  "own_wins": r["estimate"]["own_wins"], **r}
    (RES / "exploratory_g2_by_scenario.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for g, r in out.items():
        e, c = r["estimate"], r["ci95"]["rd"]
        print(f"{g:7s} units={r['units']:3d} samples={r['samples']:5d} rd={e['rd']:.3f} ({c[0]:.3f} to {c[1]:.3f})")


if __name__ == "__main__":
    main()
