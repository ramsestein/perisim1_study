# Aggregate results

Every number of the article comes from these files. No patient-level rows; no cell under 10 patients.

- `confirmatory/phase1_O1_*.json`, `phase1_O2_*.json`: pre-registered phase (OSF 10.17605/OSF.IO/YPBVH), one file
  per outcome and destination; `phase1_new_outcomes.md` is the rendered report with the confirmatory summary.
- `confirmatory/first_run_deviation/`: the first run, before the logistic recalibration was corrected (the
  deviation dated in the decision log); verdicts are the same.
- `exploratory/hypotension/`: adopt, update or build (`own_vs_external_*`), closed test, own-model variants and Riley
  (`r8_*`), vasopressor stratum (`vaso_strata.*`) and the semi-synthetic map (`shift_map_*`).
- `exploratory/t2/`: the same analyses for the ordinal stay after ICU and death.

In each JSON, `by_n` holds one entry per number of local patients: mean test log-loss of every option
(`logloss_mean`), pairwise differences with the share of simulated hospitals each option wins (`own_vs_update`,
…), and the regret of each choice procedure (`policies`).
