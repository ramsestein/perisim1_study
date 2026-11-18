# Analysis scripts

These are the scripts that produced the aggregate results in `../results/`, copied from the full PERISIM archive.
They are here so that every analysis of the article can be read next to its output. Except `phase2_g2_by_scenario.py`, they do **not** run on their
own: they import the PERISIM packages (`hypo`, `perisim`, the frozen T2 code and `review_analyses.py`) and read
the frozen artefacts and the PhysioNet databases, all of which live in the full archive.

| Script | What it produces | Results |
|---|---|---|
| `phase1_new_outcomes.py` | Pre-registered phase: external LightGBM per destination, the three options and the own-model variants, cross-validation, closed test, rules v1 and v2, H1 to H3 | `results/confirmatory/` |
| `phase2_realism.py` | Phase 2 (OSF SAJEX): single eICU-CRD hospitals (H), MIMIC-IV over time (T), harmonization errors M0–M3 (M); balanced options; G1 to G4 | `results/confirmatory_phase2/phase2_*` |
| `phase2_g2_by_scenario.py` | Exploratory: accuracy of the per-sample shift diagnostic by scenario, with the registered G2 estimator. Runs on its own (numpy) from the phase 2 aggregates | `results/confirmatory_phase2/exploratory_g2_by_scenario.json` |
| `phase2_sensitivity.py` | Exploratory (internal review 9): `--margin` re-reads the cached phase 2 samples with a minimum win margin; `--set N` re-runs the 7 NWICU units with balanced options | `results/sensitivity/phase2_margin.json`, `phase2_N.json` |
| `posthoc_t2_balanced.py` | Exploratory: T2 with balanced update and build | `results/sensitivity/t2_balanced.json` |
| `own_ext_common.py` | Shared helpers: rules, closed test, net benefit, Riley sizes, hypothesis readings, guarded logistic recalibration | — |
| `phase0_new_outcomes.py` | Phase 0 counts and prevalences of the new outcomes (the only step run before registration) | in the protocol |
| `posthoc_own_vs_external.py` | Hypotension: adopt, update or build; cross-validated choice; shift diagnostics (its PRAM replica is reported in the separate perisim_knn_nca study) | `results/exploratory/hypotension/own_vs_external_*` |
| `posthoc_r8_hypo.py` | Hypotension: closed test, net benefit, own-model variants, Riley | `results/exploratory/hypotension/r8_*` |
| `posthoc_t2_own.py`, `posthoc_r8_t2.py` | The same for T2 (ordinal stay after ICU and death) | `results/exploratory/t2/` |
| `posthoc_vaso_strata.py` | Calibration in the vasopressor stratum | `results/exploratory/hypotension/vaso_strata.*` |
| `posthoc_shift_map.py` | Semi-synthetic map of level and relation shift | `results/exploratory/hypotension/shift_map_*` |

To run them: obtain the four databases from PhysioNet, check out the full PERISIM archive, place these scripts in
its `scripts/` folder (they are already there) and follow its README. The decisions behind each script, dated
before it ran, are in `../preregistration/decision_log_excerpt.md`.
