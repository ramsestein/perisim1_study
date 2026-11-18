# Decision log (excerpt)

Entries of the dated decision log of the full PERISIM archive (docs/DECISIONS.md) that define the analyses of this article, copied verbatim. The full log is in the Zenodo archive.

## 2026-11-17 — Internal review 7: when is the hospital's own model better than the external one? (written before anything runs)

The question a receiving hospital asks is not which recalibration to use but whether to adopt the external model,
update it, or build its own. Block N, R1 and R2 answer it at a few sizes with one draw; review 7 answers it with
replicate draws and with the decision the hospital would actually make from its own sample. A replica of PRAM
(Jeong et al., 2026, medRxiv) is added, because the stacking arm is only a relative of it. Post hoc, exploratory,
reported descriptively. Thresholds below were fixed after hypotension (block N) and T2 (R2) had been read; they are
labelled as such.

**R3. Adopt, update or build (`scripts/posthoc_own_vs_external.py` for `hypo`, every unit incl. NWICU;
`scripts/posthoc_t2_own.py` for T2, MIMIC-IV and eICU).** Three options a hospital can take with n local patients:
*adopt* (the transported LightGBM with logistic recalibration; offsets + common slope on T2), *update* (LightGBM
boosted from the transported model) and *own* (LightGBM fitted from scratch on the local patients), block N's fixed
settings. `hypo`: n ∈ {250, 500, 1,000, 2,000, 4,000} patients below the smallest fold (5, 5, 5, 3, 3 draws), within
each outer fold (the fold's test landmarks score every option); T2: n ∈ {250, 500, 1,000, 2,000, 4,000, 8,000}, R2's
draws and test set (R2's cached predictions are reused). Readings fixed now, per unit:
- Break-even size: the smallest n at which *own* has a lower mean test log-loss than *adopt*, and the smallest n at
  which *own* wins in at least 80 % of the hospital samples (draw × fold); the same for *update* vs *adopt* and
  *own* vs *update*.
- Decision from the hospital's own sample: the hospital chooses the option with the lowest log-loss in a 3-fold
  patient-grouped cross-validation on its n patients, refits it on all n and deploys it. Reported: share of samples
  in which the chosen option is the best on the test set, and the regret (test log-loss of the chosen option minus
  the best option's) of this policy and of the fixed policies always-adopt, always-update and always-own.
- What predicts the gap: in each sample, the calibration slope of the transported model on the n local patients
  and the gap between its expected AUROC (outcomes simulated from the intercept-recalibrated predictions) and its
  observed AUROC on those patients; Spearman correlation of each with the realised test gap (own − adopt). A rule
  fixed now, after reading hypotension and T2 (so not a test): "relation shift" when the slope is below 0.8 or the
  AUROC gap exceeds 0.03; then *update* if n ≥ 500, otherwise *adopt*; its regret is reported next to the others.

**R4. PRAM replica (`hypo` only, binary outcome as in PRAM; same samples as R3).** Base models frozen from the
development pool: the transported LightGBM and a logistic regression fitted on the development pool as the LightGBM
was (`compare.fit("logreg")`). Bank: the n local patients' landmarks; Euclidean distance on the development pool's
neutral encoding (the `euclidean` comparator's axes), neighbours as distinct patients (our case-base rule; PRAM uses
rows), k = 50, inverse-distance-weighted mean of the neighbours' outcomes; p = (1 − α)·p_base + α·p_kNN, α on
{0, 0.1, …, 1} chosen on 20 % of the n patients held out with the other 80 % as bank, then the bank is all n
patients; PRAM + isotonic: isotonic regression fitted on the held-out 20 %'s PRAM outputs. Readings: PRAM vs its
unadapted base (PRAM's own comparison), vs the logistic recalibration of the same base (the comparison PRAM leaves
out), and vs *own*.

## 2026-11-17 — Internal review 8: closing the decision analyses (written before anything runs)

Review 7's decision results are exploratory and rest on one model family with fixed settings, log-loss only and a
diagnostic rule fixed after reading the data. Review 8 adds four analyses on the same samples (same draws, folds and
seeds as review 7; the options are refitted because review 7 kept no predictions). Post hoc, exploratory, reported
descriptively. A third outcome to test the rule prospectively is pre-registered separately
(`docs/prereg_third_outcome.md`) and is not part of this entry.

**R5. Three ways to decide, same samples.** Besides the 3-fold cross-validated choice and the rule of review 7, the
closed testing procedure of Vergouwe et al. (2017) as adapted in `roll` (`src/roll/ml.py`): the n patients split 2:1
by a seeded draw; candidates fitted on two thirds, scored on one third; one-sided tests (α = 0.05) on per-patient
sums of log-loss differences; top-down among the nested recalibrations (logistic against keep; if better, logistic
against intercept), then update against the recalibration chosen, then own against the option chosen so far; the
chosen candidate refitted on the n patients. T2: the same with the multinomial recalibrations (offsets; offsets +
common slope) as the nested steps. Reported: share of samples in which each procedure picks the best of adopt,
update and own on the test set; mean and 90th-percentile regret against that best (keep or intercept chosen by the
closed test are scored as they are, so their regret can be negative).

**R6. Clinical utility and sample size.** Net benefit per prediction of each option: `hypo` at thresholds 0.10, 0.20
and 0.30; T2 for death (thresholds 0.02, 0.05, 0.10) and for long stay or death (0.30, 0.40, 0.50). Reported: mean
difference own − adopt and update − adopt per 100 predictions and the share of samples above 0. Events in each
sample (`hypo`: landmarks with hypotension and patients with ≥ 1; T2: deaths and long stays or deaths). The
minimum sample size of Riley et al. (2020) for developing a regression model in each destination (criteria 1–3,
shrinkage 0.9, δ = 0.05, precision of the intercept ± 0.05), with p = the number of local inputs and the
anticipated Cox–Snell R² of the adopted model on all local labels (per landmark in `hypo`, converted to patients with
the mean landmarks per patient; T2 per stay, for death against the rest and for long stay or death against the rest,
the larger reported); set beside the empirical break-even sizes. Approximate by construction; read as an order of
magnitude.

**R7. Is the conclusion an artefact of fixed LightGBM settings?** Two more own-model arms on every sample: LightGBM
with num_leaves ∈ {7, 15, 31} × min_data_in_leaf ∈ {20, 100} chosen by 3-fold patient-grouped CV in the sample
(learning rate 0.05, early stopping as before), and an L2 logistic regression (`hypo`: medians imputed, missing
indicators, one-hot categories, standardised; T2: the transport encoding, standardised; C ∈ {0.01, 0.1, 1} by the same
inner CV). Reported as in review 7 (break-even, share of wins), with own = the best of the three own arms on the test
set as an upper bound (labelled as such: it uses the test set).

**R8. The vasopressor stratum in every unit.** With all local labels: in landmarks with and without a vasopressor
running (`vaso_on`), calibration in the large and slope of the transported LightGBM after logistic recalibration
fitted on all strata, and the log-loss difference recalibrated − own (block N's scratch fit) and recalibrated −
update, with patient-bootstrap 95 % CIs (1,000), in the six `hypo` units. Reading fixed now: the vasopressor failure
replicates in a unit when the recalibrated model's calibration in the large in the vasopressor stratum has a 95 % CI
entirely beyond ± 0.10, or the recalibrated − own gap in that stratum exceeds the gap in the other stratum with
non-overlapping CIs.

## 2026-11-17 — New outcomes: registration and Phase 1 (written after registration, before any model is fitted)

docs/prereg_third_outcome.md was registered on OSF on 2026-11-17: **10.17605/OSF.IO/YPBVH**. Only Phase 0 (counts and
prevalences) had run. Phase 1 runs as registered with `scripts/phase1_new_outcomes.py` (external LightGBM per
destination through `compare.fit("lightgbm")` with the frozen seed, cached once in review/units/phase1; review 7's
sizes, draws, seeds and options; review 8's own-model variants, closed test and net benefit; rules v1 and v2).
Operational readings fixed now, before the run, where the registration left a detail open:

- **Units.** O1: MIMIC-IV, eICU-CRD, NWICU (3). O2: INSPIRE, MIMIC-IV, eICU-CRD and NWICU from each of the three
  rotation pairs (6). Each counts as one unit in H1–H3.
- **"Own" in H1** is the registered own option (LightGBM from scratch, fixed settings); "beats" is the break-even of
  section 4 (≥ 80 % of samples with a lower test log-loss).
- **"With n ≥ 1,000" in H2 and H3** is read at each size n ≥ 1,000 separately: every such size must meet the bound.
- **Not evaluable.** A unit whose sizes cannot decide H1 (relation shift with no break-even and largest n < 2,000;
  level shift with no break-even against update and largest n < 4,000) or that has no size ≥ 1,000 (H2, H3) is
  reported as not evaluable for that hypothesis and counted apart; it is neither a pass nor a failure.
- **Closed test regret** is against the best of adopt, update and own, as in review 8, so it can be negative when the
  closed test keeps the model or refits only the intercept.

## 2026-11-18 — Phase 1 deviation: the logistic recalibration diverged in one unit (written before the rerun)

Reading the first Phase 1 run, one unit (O2, destination INSPIRE, external model from MIMIC-IV + eICU-CRD) showed an
adopt log-loss of 6.4 nats and an adopt AUROC of 0.51–0.53 against 0.628 for the unrecalibrated model. A logistic
recalibration is monotone and cannot change the AUROC except to 1 − AUROC, so this is a numerical failure, not a
result: the plain Newton fit shared by every review script (`posthoc_paper._logistic`, no step control) diverged on
this external model's saturated, wrong-way logits (reproduced in tests). In the other eight units the adopt AUROC
equals the unrecalibrated AUROC to three decimals at every size, and in internal review 7 (all 24 unit × size cells)
likewise, so the failure is confined to this unit.

Correction, before any rerun: Phase 1 uses `own_ext_common.logistic_guarded`, the same likelihood with step-halving,
which returns the same estimate whenever plain Newton converges (tested to 1e-7) and does not diverge otherwise. It
replaces the fit everywhere it enters Phase 1 (adopt, intercept, the closed test's recalibrations, the calibration
slope of the diagnostic, Riley's R²). All nine units are rerun into a fresh sample cache (units/phase1_v2) with the
same external models, draws and seeds, so every unit is computed with the same code; the first run is kept as
results/review/phase1_v1 and reported as the deviation. Hypotheses, readings and thresholds are unchanged.

## 2026-11-18 — Internal review of the manuscript and a second pre-registration (written before any of it runs)

An internal review of the manuscript found that H1 compared each arm with a different option, that simulated
hospitals were random samples of one database, that harmonization between external and local data was ideal, and
that update and build were handicapped (20 % held out for early stopping, no refit; only build had a tuned variant).
The text is corrected accordingly (H1 kept as registered and declared to hold as written; the diagnosis no longer
claimed to tell when to build). A second pre-registration, docs/prereg_realism_harmonization.md, fixes three new sets
of units (single eICU-CRD hospitals, MIMIC-IV over time, controlled harmonization errors), balanced options and four
hypotheses (G1–G4) before any model is fitted for them. Only its Phase 0 counts have run.

## 2026-11-18 — Second pre-registration registered (OSF 10.17605/OSF.IO/SAJEX); operational readings (before any run)

docs/prereg_realism_harmonization.md was registered on OSF: **10.17605/OSF.IO/SAJEX**. It runs with
`scripts/phase2_realism.py`. Readings fixed now where the text leaves a detail open:

- **Cross-validated choice inside a sample** uses the same balanced options as the sample itself (iterations chosen
  by an inner 3-fold patient-grouped CV in each outer fold, then refitted on that fold's fitting patients).
- **Closed test**: the 2:1 split fits keep, intercept, logistic, update and build (update and build with the balanced
  iteration rule on the two-thirds); the chosen label is scored with that option refitted on all n patients.
- **G4** is read on cells: each cell's mean regret over its samples, then the median and the 90th percentile of those
  cell means; the 75 % criterion counts cells whose mean cross-validation regret is ≤ the closed test's.
- **G3(a)**: a stratified (Mantel extension) linear trend test across M0–M3, unit as stratum, scores 0–3, one-sided.
- **G2** pools every sample; the cluster bootstrap resamples units with replacement.
- **Set T**: patients without an `anchor_year_group` are dropped; landmarks of the local pool are drawn by patient.
- **Set M**: the perturbations touch a copy of the inputs given to the external model only; `surgical_group` is set to
  the string "unmapped" (unseen by the external encoder, which maps it to its unknown level).


## 2026-11-18 — phase 2: aggregation bug (no change to any result)

The first set-M process to finish (O1 units) stopped at the final aggregation with `KeyError: 'set'`. Cause: on
Windows, `glob("phase2_[HTM]*.json")` ignores case, so it also read `phase2_hypotheses.json` (written when set T
finished) as if it held units. Every unit's samples and its results file had been written before the error. Fix:
the aggregation skips `phase2_hypotheses.json`, and `hypotheses()` keeps only entries that carry a set. Processes
already running keep the old code in memory and will stop at the same step; once all have finished, one cached
re-run aggregates every results file. No estimate, threshold or reading changes.

## 2026-11-19 — Internal review 9: sensitivity analyses of phase 2 (written before any of them runs)

An internal review of the manuscript asked (i) whether the first part's headline ("building never beats updating up
to 4,000 patients") survives balanced options in the units not covered by set M0, and (ii) how much of the per-sample
wins is noise, since a win counted at any loss difference. Three exploratory analyses, not registered, reported
descriptively next to the registered results:

- **Wins with a minimum margin (`scripts/phase2_sensitivity.py --margin`).** No model is refitted: the cached phase 2
  samples are re-read and a win counts only when the log-loss difference exceeds m ∈ {0, 0.001, 0.002} nats. Reported:
  build vs update and best own vs best external by unit and size; the G2 estimator (risk difference flagged −
  unflagged, unit-clustered bootstrap, 2,000 replicates, seed 0) by scenario (H, T, M0, M1–M3, H+T+M0, all).
  m = 0 reproduces the registered numbers and is the check.
- **NWICU with balanced options (`scripts/phase2_sensitivity.py --set N`).** The 7 NWICU units of the first part
  (hypotension from each rotation model; O1 from MIMIC-IV + eICU; O2 from each pair of systems), the same external
  models and folds, phase 2's balanced options (iterations by inner 3-fold CV, refit on all n; tuned variants) and no
  induced error; n = 250, 500, 1,000 (NWICU's ceiling), 2 draws within each of the 5 folds. Reading: break-even of
  build vs update and of update vs adopt; whether building beats updating in ≥ 80 % of samples anywhere.
- **T2 with balanced options (`scripts/posthoc_t2_balanced.py`).** R2's draws, transported model and test set; update
  (multiclass boosting from the transported model) and build (from scratch) with iterations by inner 3-fold
  patient-grouped CV and refit on all n; adopt = offsets + common slope. Same reading as above.

Together with set M0 these cover all 17 units of the first part with balanced options. Nothing in the registered
hypotheses changes; the manuscript's Table 2 will show the balanced break-evens next to the original ones.
