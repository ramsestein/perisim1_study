# Pre-registration — adopt, update or build: new outcomes to test the decision rules

Registered 2026-11-17: OSF 10.17605/OSF.IO/YPBVH (https://doi.org/10.17605/OSF.IO/YPBVH).
Written before any model is fitted for these outcomes; only Phase 0 (counts and
prevalences, section 7) has run. Repository: github.com/ramsestein/perisim (this file: docs/prereg_third_outcome.md).
Related registrations: OSF 10.17605/OSF.IO/P5CA3, 10.17605/OSF.IO/NAQ2T, 10.17605/OSF.IO/UHYDS.

## 1. Why

Internal reviews 7 and 8 (docs/DECISIONS.md, 2026-11-17) found two regimes. In hypotension (a level shift), a
hospital's own model never beat the external model updated with local data and beat the adopted (recalibrated)
model only with 2,000–4,000 patients. In T2 (a change in the predictor–outcome relation), the own model won from
500–1,000 patients. Two diagnostics measured on a few hundred local patients (the calibration slope of the external
model and the gap between its expected and observed AUROC) separated the regimes, and cross-validation inside the
hospital's own sample chose well. The thresholds of the diagnostic rule were fixed after reading those two outcomes,
so the rule has not been tested. This study tests it, and the cross-validated choice, on outcomes not yet analysed.

## 2. Outcomes (carried by the existing `hypo` landmarks; no new extraction)

Population, landmarks and inputs are those of `hypo` v0.6 (docs/design_hypotension.md; normotensive landmarks every
2 h, 2–48 h after ICU admission, inputs known at L).

- **O1, vasopressor start** (`vaso_start`): a vasopressor infusion starts in [L, L + 6 h), among landmarks with no
  vasopressor running at L. Systems: MIMIC-IV, eICU-CRD and NWICU. INSPIRE does not record running infusions and is
  excluded.
- **O2, ICU discharge within 24 h** (`icu_discharge_24h`): the ICU stay ends in (L, L + 24 h], all landmarks (a
  death in the ICU within 24 h counts as not discharged). Systems: INSPIRE, MIMIC-IV, eICU-CRD and NWICU.

## 3. Design

- **External model.** For each destination, a LightGBM fitted on the other systems exactly as `hypo`'s transported
  LightGBM (`compare.fit("lightgbm")`: same grid, inner folds and temperature scaling), frozen. O1: destinations
  MIMIC-IV (source eICU-CRD), eICU-CRD (source MIMIC-IV) and NWICU (source MIMIC-IV + eICU-CRD). O2: the `hypo`
  rotation (each of INSPIRE, MIMIC-IV, eICU-CRD from the other two) and NWICU (from each rotation pair).
- **Three options** with n local patients, as review 7: adopt (logistic recalibration), update (LightGBM boosted from
  the external model), own (LightGBM from scratch; fixed settings), plus review 8's own-model variants (tuned
  LightGBM; L2 logistic regression).
- **Sizes and samples.** n ∈ {250, 500, 1,000, 2,000, 4,000} below the smallest training fold; 5 draws for n ≤ 1,000
  and 3 above, within each of 5 patient folds; scored on the fold's test landmarks.
- **Decision procedures**, all fixed now:
  - CV: 3-fold patient-grouped cross-validation on the n patients among adopt, update and own;
  - closed test: Vergouwe et al. (2017) as adapted in `roll` (review 8, R5);
  - rule v1 (frozen 2026-11-17, review 7): relation shift if slope < 0.8 or expected − observed AUROC > 0.03; then
    update if n ≥ 500, else adopt; otherwise adopt;
  - rule v2 (fixed now, from reviews 7–8, before these outcomes): relation shift as in v1; then own if n ≥ 1,000,
    else adopt; level shift: adopt, and update if n ≥ 4,000.
- **Primary metric**: log-loss on the test landmarks; secondary: AUROC, net benefit at thresholds fixed now (O1:
  0.05, 0.10, 0.20; O2: 0.30, 0.50, 0.70).

## 4. Hypotheses (confirmatory) and decision rules

For each unit, the **regime label** is the majority vote of rule v1's diagnostic over all samples with n = 250 to
1,000 (relation shift if ≥ 50 % of them are flagged). The **break-even** of own against adopt is the smallest n at
which own has a lower test log-loss in ≥ 80 % of the samples; of own against update, likewise.

- **H1 (the diagnosis anticipates the answer).** In every unit labelled relation shift, own beats adopt at some
  n ≤ 2,000; in every unit labelled level shift, own does not beat update at any n ≤ 4,000. H1 holds if it holds in
  all units of both outcomes; a single exception is reported as a partial failure, two or more as a failure.
- **H2 (cross-validation chooses safely).** With n ≥ 1,000, the mean regret of the CV choice (test log-loss of the
  chosen option minus the best of adopt, update, own) is ≤ 0.002 nats in every unit.
- **H3 (rule v2 against CV).** With n ≥ 1,000, rule v2's mean regret is not more than 0.002 nats above CV's in any
  unit.

Secondary (descriptive): the closed test against CV (correct share, regret); rule v1; break-even sizes of each
own-model variant; Riley et al. (2020) minimum sample size per destination beside the break-even; net benefit
differences.

## 5. Phase 0 (allowed before registration)

Counts of landmarks, patients and outcome prevalence per system and outcome, with the share of landmarks off
vasopressors (O1). No model is fitted and no association with any input is computed before registration.

## 6. Deviations and stopping

A unit with fewer than 1,000 patients in its smallest training fold drops the sizes it cannot reach. A unit whose
external model cannot be fitted (fewer than 100 events in the source) is dropped and reported. Any deviation is
dated in docs/DECISIONS.md before the run it affects.

## 7. Phase 0 results (run 2026-11-17, before registration; normotensive, observable landmarks)

| system | landmarks | stays | O1 landmarks (off vasopressor) | O1 prevalence | O1 events | O2 prevalence | O2 events |
|---|---|---|---|---|---|---|---|
| INSPIRE | 148,293 | 12,454 | not measured (no infusion records) | — | — | 0.587 | 87,070 |
| MIMIC-IV | 387,158 | 26,295 | 305,427 | 0.022 | 6,865 | 0.365 | 141,441 |
| eICU-CRD | 466,384 | 33,401 | 433,173 | 0.026 | 11,210 | 0.418 | 194,957 |
| NWICU | 30,833 | 2,061 | 26,874 | 0.024 | 648 | 0.486 | 14,987 |

O1 is rare (2–3 % of landmarks): at n = 250 local patients a sample holds a few dozen events, so its smallest sizes
are expected to be noisy; the sizes stay as planned.
