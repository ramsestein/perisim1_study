# Analysis scripts

These are the scripts that produced the aggregate results in `../results/`, copied from the full PERISIM archive.
They are here so that every analysis of the article can be read next to its output. They do **not** run on their
own: they import the PERISIM packages (`hypo`, `perisim`, the frozen T2 code and `review_analyses.py`) and read
the frozen artefacts and the PhysioNet databases, all of which live in the full archive.

| Script | What it produces | Results |
|---|---|---|
| `phase1_new_outcomes.py` | Pre-registered phase: external LightGBM per destination, the three options and the own-model variants, cross-validation, closed test, rules v1 and v2, H1 to H3 | `results/confirmatory/` |
| `own_ext_common.py` | Shared helpers: rules, closed test, net benefit, Riley sizes, hypothesis readings, guarded logistic recalibration | — |
| `phase0_new_outcomes.py` | Phase 0 counts and prevalences of the new outcomes (the only step run before registration) | in the protocol |
| `posthoc_own_vs_external.py` | Hypotension: adopt, update or build; cross-validated choice; shift diagnostics; PRAM replica | `results/exploratory/hypotension/own_vs_external_*` |
| `posthoc_r8_hypo.py` | Hypotension: closed test, net benefit, own-model variants, Riley | `results/exploratory/hypotension/r8_*` |
| `posthoc_t2_own.py`, `posthoc_r8_t2.py` | The same for T2 (ordinal stay after ICU and death) | `results/exploratory/t2/` |
| `posthoc_vaso_strata.py` | Calibration in the vasopressor stratum | `results/exploratory/hypotension/vaso_strata.*` |
| `posthoc_shift_map.py` | Semi-synthetic map of level and relation shift | `results/exploratory/hypotension/shift_map_*` |

To run them: obtain the four databases from PhysioNet, check out the full PERISIM archive, place these scripts in
its `scripts/` folder (they are already there) and follow its README. The decisions behind each script, dated
before it ran, are in `../preregistration/decision_log_excerpt.md`.
