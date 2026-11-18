"""Build docs/data/study.json, the data behind the web version of the article, from the aggregate results in
results/. Pure standard library; run from the repository root:  python site/build_data.py
"""

from __future__ import annotations

import json
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


def main() -> None:
    conf, verdict = confirmatory()
    data = {"units": hypotension() + t2() + conf, "hypotheses": verdict,
            "registration": "10.17605/OSF.IO/YPBVH"}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(data['units'])} units; {verdict}")


if __name__ == "__main__":
    main()
