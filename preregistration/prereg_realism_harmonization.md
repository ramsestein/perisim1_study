# Pre-registration — update before you build, under realistic conditions: single hospitals, time and imperfect harmonization

Registered 2026-11-18: OSF 10.17605/OSF.IO/SAJEX (https://doi.org/10.17605/OSF.IO/SAJEX).
Written after the first confirmatory phase (OSF 10.17605/OSF.IO/YPBVH;
results in results/review/phase1) and after an internal review of the manuscript, and before any model is fitted
for the analyses below. Only Phase 0 (counts and prevalences, section 8) has run. Repository:
github.com/ramsestein/perisim (this file: docs/prereg_realism_harmonization.md). Related registrations: OSF
10.17605/OSF.IO/YPBVH, 10.17605/OSF.IO/P5CA3, 10.17605/OSF.IO/NAQ2T, 10.17605/OSF.IO/UHYDS.

## 1. Why

The first confirmatory phase found that, in 9 units on two new outcomes, a model built from scratch never beat the
external model updated with local data up to 4,000 local patients. An internal review raised four limits that this
study addresses:

1. **Simulated hospitals were random samples of a database**, and eICU-CRD as a destination mixes 208 hospitals. We
   now use single eICU-CRD hospitals as destinations, and a temporal split in MIMIC-IV (train on the past, predict
   the future).
2. **Harmonization was ideal**: the external and the local model shared extraction, definitions and units. A
   vendor or published model usually does not. We now introduce controlled harmonization errors between the data the
   external model expects and the data the hospital feeds it.
3. **The options were not balanced**: update and build reserved 20 % of the local patients for early stopping and were
   not refitted on all of them, and only the own model had a tuned variant. Both are corrected here.
4. **The shift diagnosis was tested with a different comparator in each arm and only at the level of the unit.** We
   now test it per sample, as a hospital would use it, against one comparator: the best own model against the best
   option built on the external model.

## 2. Data and outcomes

Population, landmarks (every 2 h, 2–48 h after ICU admission, normotensive and observable), inputs and outcomes are
those of the `hypo` landmarks (docs/design_hypotension.md) and of the first confirmatory phase:

- **Hypotension** within 6 h (hourly median MAP < 65 mmHg in [L, L + 6 h)).
- **O1, vasopressor start** within 6 h, among landmarks with no vasopressor running at L.
- **O2, ICU discharge** within 24 h.

## 3. Three sets of units

**Set H — single eICU-CRD hospitals.** Every eICU-CRD hospital with at least 600 patients in the `hypo` landmarks
(15 hospitals; section 8). Outcomes: hypotension and O2. O1 is excluded at this level because several hospitals
record no vasopressor infusions. External model: the frozen model already transported to eICU-CRD (hypotension: the
rotation LightGBM trained on INSPIRE + MIMIC-IV; O2: the first confirmatory phase's LightGBM trained on INSPIRE +
MIMIC-IV). Within each hospital, patients are split into 5 folds; local samples of n patients are drawn from the
training folds and scored on the test fold. Sizes: n ∈ {100, 250, 500}, each kept only if below the smallest
training fold of that hospital; 5 draws per size and fold. 30 units (15 hospitals × 2 outcomes).

**Set T — MIMIC-IV over time.** Patients are split by `anchor_year_group` (MIMIC-IV hosp/patients): local pool
2008–2016, test set 2017–2022. External model: the frozen model transported to MIMIC-IV for each outcome
(hypotension: INSPIRE + eICU-CRD; O1: eICU-CRD; O2: INSPIRE + eICU-CRD). Sizes n ∈ {250, 500, 1,000, 2,000, 4,000}
drawn from the local pool; 10 draws up to 1,000 and 5 above; all scored on the same 2017–2022 test set. 3 units.

**Set M — imperfect harmonization.** The units of the rotation (destinations INSPIRE, MIMIC-IV and eICU-CRD for
hypotension and O2; MIMIC-IV and eICU-CRD for O1; 8 units), with the external model fed data that differ from what it
was trained on. Four levels, fixed now; each includes the previous one:

- **M0** — none (the first phase's condition).
- **M1, units**: lactate × 9.01 (mmol/L read as mg/dL), creatinine × 88.4 (mg/dL read as µmol/L), haemoglobin × 10
  (g/dL read as g/L), temperature × 1.8 + 32 (°C read as °F).
- **M2, definitions and unrecorded inputs**: `map_min_6h` replaced by `map_mean_6h` (another aggregation of the same
  signal); `vent_on`, `sedation_on` and `sedation_24h` missing (not recorded by the hospital).
- **M3, coding**: `surgical_group` set to an unmapped category and `emergency` missing.

The errors affect only what the external model sees: adopt recalibrates the external predictions computed on the
perturbed inputs, update starts from that perturbed logit, and the diagnosis is read on those predictions. The
hospital's own data, which update and build learn from, stay as recorded. Sizes n ∈ {250, 1,000, 4,000}, 5 folds ×
2 draws per size, as in the first phase. 32 unit-levels (8 units × 4 levels).

## 4. Options, made comparable

With n local patients the hospital can:

- **adopt**: logistic recalibration (intercept and slope) of the external logit, fitted by maximum likelihood with
  step-halving (as corrected in the first phase);
- **update**: a LightGBM on local labels that starts from the external logit (fixed settings: learning rate 0.05,
  31 leaves, 50 observations per leaf, row and column subsampling 0.8);
- **build**: the same LightGBM from scratch.

**Change from the first phase (fixed now):** for update and build, the number of boosting iterations is chosen by
3-fold patient-grouped cross-validation on the n patients (mean of the per-fold best iterations, early stopping with
patience 50, at most 2,000), and the model is then refitted on all n patients with that number. Variants, with the
same iteration rule: **update_tuned** and **build_tuned** (num_leaves ∈ {7, 15, 31} × min_data_in_leaf ∈ {20, 100}
chosen by the same inner cross-validation) and **build_lr** (L2 logistic regression, C ∈ {0.01, 0.1, 1}; medians
imputed, missing indicators, one-hot categories, standardised).

The **best external option** of a sample is the lower test log-loss of adopt, update and update_tuned; the **best own
option** is the lower of build, build_tuned and build_lr. Both are read on the test set and are labelled as upper
bounds; the primary comparisons use the fixed-setting update and build.

## 5. Diagnosis and choice

- **Diagnosis**, per sample, on the n patients: calibration slope of the external model and expected (case-mix,
  20 simulations) minus observed AUROC; flag = slope < 0.8 or gap > 0.03 (thresholds of the first phase, unchanged).
- **Choice procedures** among adopt, update and build: 3-fold patient-grouped cross-validation (choose and refit on
  all n); the closed-testing procedure inspired by Vergouwe et al. (2017) as in the first phase (labels chosen on a
  2:1 split; the chosen option is then scored refitted on all n); rule v2 of the first phase.
- **Regret** = test log-loss of the chosen option minus the best of adopt, update and build.

## 6. Hypotheses (confirmatory) and decision rules

"Beats" = a lower test log-loss in at least 80 % of the samples of that unit and size.

- **G1 — updating is not beaten in realistic destinations.** In every unit of sets H and T, build does not beat
  update at any evaluated size. Holds if there is no exception; one exception is a partial failure; two or more are a
  failure.
- **G2 — the diagnosis, read on one sample, points to when building pays.** Pooling every sample of sets H, T and M,
  the share of samples in which the best own option beats the best external option is higher among flagged samples
  than among unflagged ones: risk difference > 0 with a 95 % CI (bootstrap clustered by unit, 2,000 replicates) that
  excludes 0. Sensitivity, specificity, positive and negative predictive values are reported with the same CIs.
- **G3 — harmonization errors erode the advantage of starting from the external model.** In set M, (a) the pooled
  share of samples in which the best own option beats the best external option increases from M0 to M3 (one-sided
  Cochran–Armitage trend test across levels, p < 0.05, unit as stratum), and (b) at M3 with 4,000 patients, build
  beats update in at least half of the 8 units.
- **G4 — cross-validation chooses with a small, bounded cost.** Over every unit-size cell of sets T and M with
  n ≥ 1,000: median regret of cross-validation ≤ 0.002 nats and 90th percentile ≤ 0.005 nats; and cross-validation
  has a regret no larger than the closed test in at least 75 % of those cells.

Decision rules fixed now: a hypothesis whose units cannot reach the sizes it names is reported as not evaluable for
those units (set H reaches only 500 patients, so it enters G1 only up to its sizes, and G4 not at all). No threshold
or reading above will be changed after the run.

**Secondary (descriptive)**: per unit and level, break-even sizes of build and its variants against adopt, update
and the best external option; the smallest harmonization level at which building pays; net benefit per landmark at
the thresholds of the first phase (hypotension 0.10, 0.20, 0.30; O1 0.05, 0.10, 0.20; O2 0.30, 0.50, 0.70); the
rule's and the closed test's choices; within-unit Spearman correlation between the diagnostics and the own-minus-best-
external difference.

## 7. Sensitivity re-analyses of the first phase (declared exploratory)

Run with the code of this study and labelled exploratory, not confirmatory, because they revisit data already seen:
(i) the 9 units of the first confirmatory phase and the 6 hypotension units re-run with the balanced options of
section 4; (ii) the first phase re-read with one comparator in both arms (best own against best external option)
and with the per-sample diagnosis accuracy of G2; (iii) a decomposition of O2 with INSPIRE as destination: per
sample, calibration-in-the-large and slope of adopt, and the number of iterations kept by update, at 250 and 500
patients.

## 8. Phase 0 (run 2026-11-18, before registration; normotensive, observable landmarks)

**Set H** — eICU-CRD hospitals with at least 600 patients (eICU public hospital identifiers):

| hospital | patients | landmarks | hypotension prevalence | O2 prevalence |
|---|---|---|---|---|
| 73 | 1,680 | 28,164 | 0.146 | 0.403 |
| 413 | 1,102 | 13,625 | 0.200 | 0.632 |
| 167 | 941 | 12,157 | 0.215 | 0.527 |
| 243 | 818 | 13,631 | 0.230 | 0.277 |
| 420 | 772 | 12,277 | 0.251 | 0.315 |
| 458 | 743 | 11,629 | 0.136 | 0.397 |
| 338 | 729 | 10,864 | 0.215 | 0.422 |
| 252 | 711 | 11,559 | 0.168 | 0.391 |
| 443 | 699 | 11,184 | 0.169 | 0.344 |
| 300 | 663 | 9,323 | 0.226 | 0.452 |
| 152 | 661 | 8,125 | 0.245 | 0.594 |
| 411 | 651 | 7,941 | 0.257 | 0.514 |
| 264 | 650 | 10,001 | 0.185 | 0.355 |
| 449 | 647 | 9,372 | 0.121 | 0.374 |
| 199 | 603 | 9,321 | 0.216 | 0.238 |

**Set T** — MIMIC-IV by `anchor_year_group`:

| years | patients | landmarks | hypotension prevalence | O2 prevalence | O1 prevalence (off vasopressor) |
|---|---|---|---|---|---|
| 2008–2010 | 6,942 | 112,194 | 0.320 | 0.355 | 0.024 |
| 2011–2013 | 5,929 | 92,025 | 0.313 | 0.375 | 0.025 |
| 2014–2016 | 5,356 | 83,493 | 0.316 | 0.366 | 0.027 |
| 2017–2019 | 3,686 | 57,452 | 0.293 | 0.381 | 0.022 |
| 2020–2022 | 2,551 | 41,994 | 0.256 | 0.349 | 0.007 |

Local pool 2008–2016: 18,227 patients; test 2017–2022: 6,237 patients. O1 prevalence falls in 2020–2022; the test
set is kept as defined.

## 9. Deviations and stopping

A unit whose external model or options cannot be fitted (a sample with a single outcome class in the fitting set is
scored with the identity for adopt and the training prevalence for build) is reported and kept. Any deviation is
dated in docs/DECISIONS.md before the run it affects. Results are published whatever they show.
