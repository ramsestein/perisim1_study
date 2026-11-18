"""Phase 0 of docs/prereg_third_outcome.md (allowed before registration): counts and prevalences of the two new
outcomes per system. No model, no association with any input.

Usage:  python scripts/phase0_new_outcomes.py
Output (aggregates only): <experiments>/hypo/review/phase0_new_outcomes.json and reports/phase0_new_outcomes.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import polars as pl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import review_analyses as RA  # noqa: E402,F401  (sets the frozen src on sys.path)


def summary(df: pl.DataFrame) -> dict:
    d = df.filter(pl.col("normotensive") & pl.col("known")) if "known" in df.columns else df.filter(pl.col("normotensive"))
    sid = "subject_id" if "subject_id" in d.columns else "stay_id"
    off = d.filter(~pl.col("vaso_on"))
    out = {"landmarks": d.height, "units": int(d[sid].n_unique()),
           "share_off_vasopressor": float(off.height / max(d.height, 1))}
    def rate(col, frame):
        v = frame[col].cast(pl.Float64).drop_nulls()
        if v.len() == 0:
            return {"landmarks": frame.height, "not_measured": True}
        return {"landmarks": int(v.len()), "prevalence": float(v.mean()), "events": int(v.sum()),
                "missing_share": float(1 - v.len() / max(frame.height, 1))}
    if "vaso_start" in d.columns:
        out["O1_vaso_start"] = rate("vaso_start", off)
    if "icu_discharge_24h" in d.columns:
        out["O2_icu_discharge_24h"] = rate("icu_discharge_24h", d)
    return out


def main() -> int:
    from hypo.config import workdir
    from hypo.frozen import external_dir
    import nwicu_transport as NT
    paths = {X: workdir() / "landmarks" / f"{X}.parquet" for X in RA.ROTATIONS}
    paths["nwicu"] = NT.work() / "landmarks" / "nwicu.parquet"
    res = {}
    for X, p in paths.items():
        res[X] = summary(pl.read_parquet(p)) if p.exists() else {"missing": str(p.name)}
    od = external_dir().with_name("review")
    (od / "phase0_new_outcomes.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    L = ["# Phase 0: new outcomes, counts and prevalences (docs/prereg_third_outcome.md)", "",
         "| system | normotensive landmarks | units | off vasopressor | O1 landmarks | O1 prevalence | O1 events | "
         "O2 prevalence | O2 events |", "|---|---|---|---|---|---|---|---|---|"]
    for X, r in res.items():
        if "missing" in r:
            L.append(f"| {X} | missing | | | | | | | |")
            continue
        o1, o2 = r.get("O1_vaso_start", {}), r.get("O2_icu_discharge_24h", {})
        L.append(f"| {X} | {r['landmarks']:,} | {r['units']:,} | {r['share_off_vasopressor']:.3f} | "
                 f"{o1.get('landmarks', 0):,} | {'not measured' if o1.get('not_measured') else format(o1.get('prevalence', float('nan')), '.3f')} | "
                 f"{o1.get('events', 0):,} | {'not measured' if o2.get('not_measured') else format(o2.get('prevalence', float('nan')), '.3f')} | "
                 f"{o2.get('events', 0):,} |")
    (external_dir().parent / "reports" / "phase0_new_outcomes.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
