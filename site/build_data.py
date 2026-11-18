"""Build docs/data/study.json, the data behind the web version of the article, from the aggregate results in
results/. Pure standard library; run from the repository root:  python site/build_data.py
"""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "docs" / "data" / "study.json"

SLOPE_THR, GAP_THR = 0.8, 0.03
OUTCOMES = {
    "hypo": "Hypotension within 6 h",
    "t2": "Stay after ICU discharge and death (T2)",
    "O1": "Vasopressor start within 6 h",
    "O2": "ICU discharge within 24 h",
}
SYS = {"inspire": "INSPIRE", "mimic": "MIMIC-IV", "eicu": "eICU-CRD", "nwicu": "NWICU"}


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def regret(po: dict, key: str):
    return round(po[key]["regret_mean"], 5) if key in po else None


def unit_record(uid, outcome, dest, source, status, by_n, regime, riley=None, extra=None):
    return {"id": uid, "outcome": outcome, "outcome_label": OUTCOMES[outcome], "destination": dest,
            "source": source, "status": status, "regime": regime, "by_n": by_n, "riley_patients": riley,
            **(extra or {})}


def hypotension() -> list[dict]:
    units = []
    src = {"inspire": "MIMIC-IV + eICU-CRD", "mimic": "INSPIRE + eICU-CRD", "eicu": "INSPIRE + MIMIC-IV"}
    for f in sorted((RES / "exploratory" / "hypotension").glob("own_vs_external_*.json")):
        r7 = load(f)
        r8 = load(f.with_name(f.name.replace("own_vs_external_", "r8_")))
        for name, u in r7.items():
            v8 = r8[name]
            if name.startswith("hypo_"):
                dest, source = SYS[name[5:]], src[name[5:]]
            else:
                dest, source = "NWICU", src[name.split("_")[1]]
            by_n, flags = {}, []
            for n, o in u["by_n"].items():
                o8 = v8["by_n"][n]
                lm = o["logloss_mean"] | {k: o8["logloss_mean"][k] for k in ("own_tuned", "own_lr")}
                po = o["policies"] | {"closed_test": o8["policies"]["closed_test"]}
                by_n[n] = {"logloss": {k: round(lm[k], 5) for k in ("adopt", "update", "own", "own_tuned", "own_lr")},
                           "own_minus_update": round(o["own_vs_update"]["mean"], 5),
                           "own_beats_update_share": round(o["own_vs_update"]["share_wins"], 3),
                           "own_beats_adopt_share": round(o["own_vs_adopt"]["share_wins"], 3),
                           "update_beats_adopt_share": round(o["update_vs_adopt"]["share_wins"], 3),
                           "regret": {"cv": regret(po, "cv"), "closed": regret(po, "closed_test"),
                                      "rule_v1": regret(po, "rule")}}
                if int(n) <= 1000:
                    dg = o["diagnostics_mean"]
                    flags.append(dg["slope"] < SLOPE_THR or dg["auroc_gap"] > GAP_THR)
            regime = "relation" if sum(flags) >= len(flags) / 2 else "level"
            units.append(unit_record(name, "hypo", dest, source, "exploratory", by_n, regime,
                                     round(v8["riley"]["n_patients"])))
    return units


def t2() -> list[dict]:
    a = load(RES / "exploratory" / "t2" / "t2_own.json")["cohorts"]
    b = load(RES / "exploratory" / "t2" / "r8_t2.json")["cohorts"]
    units = []
    for c in ("mimic", "eicu"):
        by_n, flags = {}, []
        for n, o in a[c]["by_n"].items():
            o8 = b[c]["by_n"][n]
            lm = o["logloss_mean"] | {k: o8["logloss_mean"][k] for k in ("own_tuned", "own_lr")}
            po = o["policies"] | {"closed_test": o8["policies"]["closed_test"]}
            by_n[n] = {"logloss": {k: round(lm[k], 5) for k in ("adopt", "update", "own", "own_tuned", "own_lr")},
                       "own_minus_update": round(o["own_vs_update"]["mean"], 5),
                       "own_beats_update_share": round(o["own_vs_update"]["share_wins"], 3),
                           "own_beats_adopt_share": round(o["own_vs_adopt"]["share_wins"], 3),
                       "update_beats_adopt_share": round(o["update_vs_adopt"]["share_wins"], 3),
                       "regret": {"cv": regret(po, "cv"), "closed": regret(po, "closed_test"),
                                  "rule_v1": regret(po, "rule")}}
            if int(n) <= 1000:
                dg = o["diagnostics_mean"]
                flags.append(dg["slope"] < SLOPE_THR or dg["auroc_gap"] > GAP_THR)
        regime = "relation" if sum(flags) >= len(flags) / 2 else "level"
        rl = b[c].get("riley", {}).get("severe", {}).get("n")
        units.append(unit_record(f"t2_{c}", "t2", SYS[c], "INSPIRE", "exploratory", by_n, regime,
                                 round(rl) if rl else None))
    return units


def confirmatory() -> tuple[list[dict], dict]:
    units, hyp = [], []
    for f in sorted((RES / "confirmatory").glob("phase1_O*.json")):
        for name, u in load(f).items():
            if "dropped" in u:
                continue
            outcome, dest = name.split("_")[0], name.split("_")[1]
            by_n = {}
            for n, o in u["by_n"].items():
                po = o["policies"]
                by_n[n] = {"logloss": {k: round(o["logloss_mean"][k], 5)
                                       for k in ("adopt", "update", "own", "own_tuned", "own_lr")},
                           "own_minus_update": round(o["own_vs_update"]["mean"], 5),
                           "own_beats_update_share": round(o["own_vs_update"]["share_wins"], 3),
                           "own_beats_adopt_share": round(o["own_vs_adopt"]["share_wins"], 3),
                           "regret": {"cv": regret(po, "cv"), "closed": regret(po, "closed_test"),
                                      "rule_v1": regret(po, "rule"), "rule_v2": regret(po, "rule_v2")}}
            h = u["hypotheses"]
            hyp.append(h)
            units.append(unit_record(name, outcome, SYS[dest], " + ".join(SYS[s] for s in u["sources"]),
                                     "confirmatory", by_n,
                                     "relation" if h["regime"].startswith("relation") else "level",
                                     round(u["riley"]["n_patients"]),
                                     {"hypotheses": {k: h[k] for k in ("H1", "H2", "H3")},
                                      "flag_share": round(h["flag_share"], 3),
                                      "patients": u["destination"]["patients"],
                                      "prevalence": round(u["destination"]["prevalence"], 4)}))
    verdict = {}
    for k in ("H1", "H2", "H3"):
        c = {s: sum(x[k] == s for x in hyp) for s in ("hold", "fail", "not evaluable")}
        if k == "H1":
            v = "holds" if c["fail"] == 0 else ("partial failure" if c["fail"] == 1 else "failure")
        else:
            v = "holds" if c["fail"] == 0 else "fails"
        verdict[k] = {**c, "verdict": v}
    return units, verdict


P2_UNIT = {"hypo": "Hypotension", "O1": "Vasopressor start", "O2": "ICU discharge"}
LEVEL_LABEL = {"M0": "No error", "M1": "Units", "M2": "+ definitions", "M3": "+ coding"}


def _p2_cell(o: dict) -> dict:
    po = o["policies"]
    return {"build_minus_update": round(o["build_vs_update"]["mean"], 5),
            "build_beats_update_share": round(o["build_vs_update"]["share_wins"], 3),
            "update_beats_adopt_share": round(o["update_vs_adopt"]["share_wins"], 3),
            "own_beats_ext_share": round(o["best_own_vs_best_ext"]["share_wins"], 3),
            "own_minus_ext": round(o["best_own_vs_best_ext"]["mean"], 5),
            "flag_share": round(o["flag_share"], 3), "samples": o["samples"],
            "regret": {"cv": round(po["cv"]["regret_mean"], 6), "closed": round(po["closed_test"]["regret_mean"], 6),
                       "rule_v2": round(po["rule_v2"]["regret_mean"], 6)}}


def phase2() -> dict:
    d = RES / "confirmatory_phase2"
    units = {}
    for f in sorted(d.glob("phase2_*.json")):
        if f.name in ("phase2_hypotheses.json", "phase2_H_O2_units.json"):
            continue
        for k, u in load(f).items():
            if isinstance(u, dict) and "set" in u:
                units[k] = u
    hyp = load(d / "phase2_hypotheses.json")
    scen = load(d / "exploratory_g2_by_scenario.json")
    hospitals, time_, harm = [], [], {}
    for k, u in sorted(units.items()):
        by_n = {str(n): _p2_cell(o) for n, o in u["by_n"].items()}
        rec = {"id": k, "outcome": u["outcome"], "outcome_label": P2_UNIT[u["outcome"]], "by_n": by_n,
               "patients": u["destination"]["patients"], "prevalence": round(u["destination"]["prevalence"], 4),
               "breakeven": u["breakeven_80pct"]}
        if u["set"] == "H":
            rec["hospital"] = k.split("_")[-1].lstrip("h")
            hospitals.append(rec)
        elif u["set"] == "T":
            time_.append(rec)
        else:
            base, level = k.rsplit("_", 1)
            dest = base.split("_")[-1]
            harm.setdefault(base, {"id": base, "outcome": u["outcome"], "outcome_label": P2_UNIT[u["outcome"]],
                                   "destination": SYS[dest], "levels": {}})["levels"][level] = by_n
    cells = []
    for k, u in units.items():
        if u["set"] in ("T", "M"):
            for n, o in u["by_n"].items():
                if int(n) >= 1000:
                    cells.append([round(o["policies"]["cv"]["regret_mean"], 6),
                                  round(o["policies"]["closed_test"]["regret_mean"], 6), u["set"]])
    # pooled share "best own beats best external" by harmonization level, with a unit-clustered bootstrap CI
    # (descriptive companion of G3; the registered test is in phase2_hypotheses.json)
    lv_pairs = {b["id"]: {L: [p[1] for p in units[f"{b['id']}_{L}"]["pairs"]] for L in LEVEL_LABEL}
                for b in harm.values()}
    rng = random.Random(0)
    ids = sorted(lv_pairs)

    def share(sel, L):
        v = [w for i in sel for w in lv_pairs[i][L]]
        return sum(v) / len(v)

    boot = {L: [] for L in LEVEL_LABEL}
    for _ in range(2000):
        sel = [rng.choice(ids) for _ in ids]
        for L in LEVEL_LABEL:
            boot[L].append(share(sel, L))
    pct = lambda v, q: sorted(v)[int(q * (len(v) - 1))]
    levels = {L: {"share": round(share(ids, L), 3), "ci": [round(pct(boot[L], .025), 3), round(pct(boot[L], .975), 3)],
                  "by_unit": {i: round(sum(lv_pairs[i][L]) / len(lv_pairs[i][L]), 3) for i in ids}} for L in LEVEL_LABEL}
    g2, g3, g4 = hyp["G2"], hyp["G3"], hyp["G4"]
    return {
        "registration": "10.17605/OSF.IO/SAJEX",
        "hypotheses": {
            "G1": {"units": hyp["G1"]["units"], "exceptions": len(hyp["G1"]["exceptions"]), "verdict": hyp["G1"]["verdict"]},
            "G2": {"rd": round(g2["estimate"]["rd"], 3), "ci": [round(x, 3) for x in g2["ci95"]["rd"]],
                   **{k: round(g2["estimate"][k], 3) for k in ("sens", "spec", "ppv", "npv")},
                   "samples": g2["estimate"]["samples"], "verdict": g2["verdict"]},
            "G3": {"share_by_level": {k: round(v, 3) for k, v in g3["own_beats_ext_share_by_level"].items()},
                   "z": round(g3["trend"]["z"], 1), "m3_n4000": len(g3["m3_n4000_build_beats_update"]),
                   "units_reaching_4000": g3["units_reaching_4000"], "verdict": g3["verdict"]},
            "G4": {"cells": g4["cells"], "median": round(g4["cv_median"], 5), "p90": round(g4["cv_p90"], 4),
                   "le_closed_share": round(g4["cv_le_closed_share"], 3), "verdict": g4["verdict"]},
        },
        "level_labels": LEVEL_LABEL, "levels": levels,
        "hospitals": hospitals, "time": time_, "harmonization": list(harm.values()), "g4_cells": cells,
        "scenarios": {k: {"units": v["units"], "samples": v["samples"], "rd": round(v["estimate"]["rd"], 3),
                          "ci": [round(x, 3) for x in v["ci95"]["rd"]],
                          "base_rate": round(v["own_wins"] / v["samples"], 3),
                          **{m: round(v["estimate"][m], 2) for m in ("sens", "ppv", "npv")}}
                      for k, v in scen.items()},
    }


def main() -> None:
    conf, verdict = confirmatory()
    data = {"units": hypotension() + t2() + conf, "hypotheses": verdict,
            "registration": "10.17605/OSF.IO/YPBVH", "phase2": phase2()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    p2 = data["phase2"]
    print(f"{OUT.relative_to(ROOT)}: {len(data['units'])} units; {verdict}; phase 2: {len(p2['hospitals'])} hospitals, "
          f"{len(p2['time'])} time units, {len(p2['harmonization'])} harmonization units, {len(p2['g4_cells'])} G4 cells")


if __name__ == "__main__":
    main()
