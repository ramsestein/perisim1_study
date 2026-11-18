# Phase 1: adopt, update or build on two new outcomes (pre-registered, OSF 10.17605/OSF.IO/YPBVH)

Log-loss per landmark on each fold's test landmarks; one sample = one draw of n local patients in one fold. Regret against the best of adopt, update and own. Break-even: smallest n with ≥ 80 % of samples won.

## O1_eicu (external model from mimic)

Destination: 433,173 landmarks, 31,605 patients, prevalence 0.026.
Regime label: level shift (0.00 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': 1000, 'own_vs_update': None, 'own_tuned_vs_adopt': 500, 'own_tuned_vs_update': 1000, 'own_lr_vs_adopt': 500, 'own_lr_vs_update': None, 'own_best_vs_adopt': 500, 'own_best_vs_update': 1000}.
H1: hold; H2: hold; H3: fail.
Riley et al. (2020): n = 8132 landmarks ≈ 594 patients (p = 46, R²cs 0.050).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0955 | 0.1031 | 0.1076 | 0.1039 | 0.0960 | 0.0019 / 0.0069 / 0.0012 / 0.0012 | 0.44 / 0.04 / 0.48 / 0.48 | {'keep': 0.92, 'logistic': 0.04, 'update': 0.04} | -0.15, -0.07, +0.00 | 84, 26 |
| 500 | 0.0951 | 0.0928 | 0.0942 | 0.0916 | 0.0912 | 0.0016 / 0.0075 / 0.0030 / 0.0030 | 0.36 / 0.08 / 0.16 / 0.16 | {'intercept': 0.12, 'keep': 0.72, 'update': 0.16} | +0.03, +0.10, +0.08 | 171, 51 |
| 1000 | 0.0950 | 0.0898 | 0.0903 | 0.0878 | 0.0894 | 0.0010 / 0.0028 / 0.0056 / 0.0056 | 0.48 / 0.48 / 0.00 / 0.00 | {'intercept': 0.36, 'keep': 0.04, 'own': 0.04, 'update': 0.56} | +0.18, +0.24, +0.15 | 357, 104 |
| 2000 | 0.0948 | 0.0862 | 0.0867 | 0.0850 | 0.0873 | 0.0003 / 0.0023 / 0.0087 / 0.0087 | 0.47 / 0.67 / 0.00 / 0.00 | {'intercept': 0.13333333333333333, 'keep': 0.06666666666666667, 'own': 0.13333333333333333, 'update': 0.6666666666666666} | +0.29, +0.33, +0.18 | 737, 211 |
| 4000 | 0.0948 | 0.0842 | 0.0844 | 0.0833 | 0.0869 | 0.0005 / 0.0005 / 0.0108 / 0.0003 | 0.47 / 0.47 / 0.00 / 0.60 | {'own': 0.13333333333333333, 'update': 0.8666666666666667} | +0.36, +0.41, +0.26 | 1423, 410 |

## O1_mimic (external model from eicu)

Destination: 305,427 landmarks, 23,056 patients, prevalence 0.022.
Regime label: relation shift (0.97 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': 2000, 'own_vs_update': None, 'own_tuned_vs_adopt': 2000, 'own_tuned_vs_update': 2000, 'own_lr_vs_adopt': 500, 'own_lr_vs_update': 500, 'own_best_vs_adopt': 500, 'own_best_vs_update': 500}.
H1: hold; H2: hold; H3: hold.
Riley et al. (2020): n = 14962 landmarks ≈ 1130 patients (p = 45, R²cs 0.027).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0946 | 0.0964 | 0.0988 | 0.0985 | 0.0952 | 0.0006 / 0.0059 / 0.0003 / 0.0003 | 0.72 / 0.00 / 0.76 / 0.76 | {'intercept': 0.44, 'keep': 0.52, 'logistic': 0.04} | -0.05, +0.06, -0.02 | 74, 38 |
| 500 | 0.0944 | 0.0967 | 0.0975 | 0.0964 | 0.0929 | 0.0005 / 0.0040 / 0.0024 / 0.0001 | 0.48 / 0.00 / 0.16 / 0.72 | {'intercept': 0.48, 'keep': 0.28, 'logistic': 0.12, 'update': 0.12} | +0.01, +0.10, -0.00 | 145, 73 |
| 1000 | 0.0942 | 0.0929 | 0.0943 | 0.0928 | 0.0907 | 0.0012 / 0.0028 / 0.0002 / 0.0016 | 0.32 / 0.08 / 0.76 / 0.20 | {'intercept': 0.44, 'keep': 0.04, 'logistic': 0.28, 'own': 0.08, 'update': 0.16} | +0.10, +0.13, -0.01 | 306, 153 |
| 2000 | 0.0940 | 0.0908 | 0.0916 | 0.0900 | 0.0894 | 0.0002 / 0.0026 / 0.0000 / 0.0008 | 0.67 / 0.33 / 1.00 / 0.00 | {'intercept': 0.13333333333333333, 'logistic': 0.4666666666666667, 'own': 0.06666666666666667, 'update': 0.3333333333333333} | +0.19, +0.17, +0.01 | 604, 300 |
| 4000 | 0.0940 | 0.0895 | 0.0899 | 0.0888 | 0.0888 | 0.0002 / 0.0001 / 0.0001 / 0.0004 | 0.67 / 0.80 / 0.80 / 0.20 | {'update': 1.0} | +0.26, +0.21, +0.02 | 1185, 593 |

## O1_nwicu (external model from mimic + eicu)

Destination: 26,874 landmarks, 1,989 patients, prevalence 0.024.
Regime label: level shift (0.05 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': None, 'own_vs_update': None, 'own_tuned_vs_adopt': None, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': 1000, 'own_best_vs_update': None}.
H1: not evaluable; H2: hold; H3: hold.
Riley et al. (2020): n = 8628 landmarks ≈ 639 patients (p = 38, R²cs 0.039).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0946 | 0.0960 | 0.1039 | 0.1037 | 0.0974 | 0.0011 / 0.0019 / 0.0012 / 0.0012 | 0.56 / 0.00 / 0.48 / 0.48 | {'intercept': 0.28, 'keep': 0.68, 'logistic': 0.04} | -0.26, -0.09, -0.05 | 80, 35 |
| 500 | 0.0946 | 0.0941 | 0.0991 | 0.0990 | 0.0951 | 0.0012 / 0.0017 / 0.0017 / 0.0015 | 0.48 / 0.16 / 0.32 / 0.32 | {'intercept': 0.32, 'keep': 0.48, 'logistic': 0.04, 'update': 0.16} | -0.06, +0.00, -0.03 | 164, 72 |
| 1000 | 0.0943 | 0.0919 | 0.0960 | 0.0937 | 0.0932 | 0.0006 / 0.0017 / 0.0025 / 0.0025 | 0.72 / 0.48 / 0.04 / 0.04 | {'intercept': 0.16, 'keep': 0.36, 'update': 0.48} | +0.03, +0.04, -0.03 | 326, 143 |

## O2_eicu (external model from inspire + mimic)

Destination: 466,384 landmarks, 32,032 patients, prevalence 0.418.
Regime label: level shift (0.29 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': 2000, 'own_vs_update': None, 'own_tuned_vs_adopt': 1000, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': 2000, 'own_lr_vs_update': None, 'own_best_vs_adopt': 1000, 'own_best_vs_update': None}.
H1: hold; H2: fail; H3: fail.
Riley et al. (2020): n = 3773 landmarks ≈ 260 patients (p = 46, R²cs 0.103).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6281 | 0.6299 | 0.6542 | 0.6481 | 0.6489 | 0.0023 / 0.0011 / 0.0028 / 0.0028 | 0.36 / 0.08 / 0.24 / 0.24 | {'intercept': 0.04, 'keep': 0.88, 'update': 0.08} | -2.19, -1.81, -0.58 | 1516, 184 |
| 500 | 0.6262 | 0.6239 | 0.6395 | 0.6332 | 0.6346 | 0.0024 / 0.0033 / 0.0020 / 0.0030 | 0.36 / 0.04 / 0.40 / 0.16 | {'keep': 0.88, 'update': 0.12} | -1.17, -0.46, -0.27 | 3055, 373 |
| 1000 | 0.6259 | 0.6187 | 0.6268 | 0.6225 | 0.6243 | 0.0021 / 0.0066 / 0.0040 / 0.0085 | 0.72 / 0.16 / 0.40 / 0.00 | {'keep': 0.68, 'logistic': 0.12, 'update': 0.2} | -0.38, +0.71, +0.34 | 6059, 745 |
| 2000 | 0.6254 | 0.6131 | 0.6171 | 0.6147 | 0.6203 | 0.0000 / 0.0035 / 0.0115 / 0.0117 | 1.00 / 0.73 / 0.07 / 0.00 | {'keep': 0.26666666666666666, 'update': 0.7333333333333333} | +0.12, +1.46, +0.69 | 12189, 1490 |
| 4000 | 0.6252 | 0.6080 | 0.6096 | 0.6088 | 0.6171 | 0.0001 / 0.0014 / 0.0173 / 0.0001 | 0.87 / 0.80 / 0.00 / 0.87 | {'keep': 0.06666666666666667, 'update': 0.9333333333333333} | +0.39, +2.15, +1.23 | 24301, 2975 |

## O2_inspire (external model from mimic + eicu)

Destination: 148,293 landmarks, 11,631 patients, prevalence 0.587.
Regime label: relation shift (0.56 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': 250, 'own_vs_update': None, 'own_tuned_vs_adopt': 250, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': 250, 'own_lr_vs_update': 250, 'own_best_vs_adopt': 250, 'own_best_vs_update': 250}.
H1: hold; H2: hold; H3: fail.
Riley et al. (2020): n = 5723653 landmarks ≈ 448921 patients (p = 48, R²cs -47670.724).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 6.3817 | 0.5987 | 0.6031 | 0.5928 | 0.5749 | 0.0060 / 0.0039 / 5.7871 / 5.7871 | 0.52 / 0.64 / 0.00 / 0.00 | {'own': 0.08, 'update': 0.92} | +16.98, +14.86, +26.67 | 1877, 212 |
| 500 | 6.8948 | 0.5695 | 0.5719 | 0.5621 | 0.5587 | 0.0029 / 0.0030 / 3.0662 / 6.3283 | 0.68 / 0.60 / 0.40 / 0.00 | {'update': 1.0} | +24.40, +21.18, +27.74 | 3703, 421 |
| 1000 | 6.5948 | 0.5471 | 0.5484 | 0.5452 | 0.5532 | 0.0020 / 0.0010 / 2.9450 / 2.9465 | 0.48 / 0.64 / 0.36 / 0.20 | {'own': 0.04, 'update': 0.96} | +19.31, +20.43, +36.90 | 7512, 850 |
| 2000 | 6.6020 | 0.5326 | 0.5319 | 0.5313 | 0.5474 | 0.0008 / 0.0010 / 2.4794 / 2.4789 | 0.47 / 0.47 / 0.20 / 0.40 | {'own': 0.06666666666666667, 'update': 0.9333333333333333} | +20.62, +21.53, +37.24 | 14954, 1697 |
| 4000 | 6.7195 | 0.5229 | 0.5220 | 0.5223 | 0.5456 | 0.0007 / 0.0011 / 2.9036 / 0.0007 | 0.60 / 0.47 / 0.13 / 0.67 | {'own': 0.13333333333333333, 'update': 0.8666666666666667} | +24.42, +23.05, +33.02 | 30014, 3391 |

## O2_mimic (external model from inspire + eicu)

Destination: 387,158 landmarks, 24,464 patients, prevalence 0.365.
Regime label: level shift (0.16 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': 2000, 'own_vs_update': None, 'own_tuned_vs_adopt': 1000, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': 1000, 'own_best_vs_update': None}.
H1: hold; H2: hold; H3: fail.
Riley et al. (2020): n = 2127 landmarks ≈ 135 patients (p = 45, R²cs 0.172).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.5639 | 0.5678 | 0.5977 | 0.5909 | 0.5885 | 0.0018 / 0.0085 / 0.0007 / 0.0007 | 0.68 / 0.00 / 0.80 / 0.80 | {'intercept': 0.4, 'keep': 0.56, 'update': 0.04} | -1.72, -1.58, -1.46 | 1443, 171 |
| 500 | 0.5634 | 0.5626 | 0.5799 | 0.5743 | 0.5760 | 0.0022 / 0.0090 / 0.0020 / 0.0022 | 0.48 / 0.08 / 0.40 / 0.36 | {'intercept': 0.4, 'keep': 0.52, 'update': 0.08} | -0.99, -0.57, -0.38 | 2909, 346 |
| 1000 | 0.5626 | 0.5545 | 0.5635 | 0.5604 | 0.5703 | 0.0017 / 0.0101 / 0.0081 / 0.0081 | 0.80 / 0.16 / 0.00 / 0.00 | {'intercept': 0.6, 'keep': 0.2, 'logistic': 0.04, 'update': 0.16} | -0.17, +0.55, -0.09 | 5803, 688 |
| 2000 | 0.5623 | 0.5485 | 0.5521 | 0.5516 | 0.5652 | 0.0000 / 0.0071 / 0.0138 / 0.0138 | 1.00 / 0.47 / 0.00 / 0.00 | {'intercept': 0.3333333333333333, 'keep': 0.06666666666666667, 'own': 0.13333333333333333, 'update': 0.4666666666666667} | +0.34, +1.51, +0.61 | 11542, 1368 |
| 4000 | 0.5625 | 0.5433 | 0.5439 | 0.5441 | 0.5633 | 0.0006 / 0.0004 / 0.0196 / 0.0004 | 0.47 / 0.53 / 0.00 / 0.53 | {'update': 1.0} | +0.70, +2.33, +1.03 | 23156, 2745 |

## O2_nwicu_from_mimic+eicu (external model from mimic + eicu)

Destination: 30,833 landmarks, 2,001 patients, prevalence 0.486.
Regime label: level shift (0.00 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': 1000, 'own_vs_update': None, 'own_tuned_vs_adopt': 1000, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': 1000, 'own_lr_vs_update': 250, 'own_best_vs_adopt': 1000, 'own_best_vs_update': 250}.
H1: not evaluable; H2: hold; H3: fail.
Riley et al. (2020): n = 4984 landmarks ≈ 324 patients (p = 38, R²cs 0.066).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6605 | 0.6872 | 0.6830 | 0.6803 | 0.6675 | 0.0023 / 0.0013 / 0.0006 / 0.0006 | 0.84 / 0.00 / 0.92 / 0.92 | {'intercept': 0.88, 'logistic': 0.12} | -0.86, -2.93, -1.44 | 1857, 206 |
| 500 | 0.6594 | 0.6589 | 0.6650 | 0.6589 | 0.6573 | 0.0040 / 0.0047 / 0.0040 / 0.0040 | 0.32 / 0.00 / 0.32 / 0.32 | {'intercept': 0.84, 'logistic': 0.12, 'update': 0.04} | -0.49, +0.07, -0.98 | 3771, 416 |
| 1000 | 0.6588 | 0.6485 | 0.6530 | 0.6493 | 0.6533 | 0.0017 / 0.0110 / 0.0113 / 0.0113 | 0.64 / 0.08 / 0.00 / 0.00 | {'intercept': 0.64, 'logistic': 0.24, 'update': 0.12} | +0.02, +1.42, +0.07 | 7484, 828 |

## O2_nwicu_from_inspire+eicu (external model from inspire + eicu)

Destination: 30,833 landmarks, 2,001 patients, prevalence 0.486.
Regime label: level shift (0.03 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': 500, 'own_vs_update': None, 'own_tuned_vs_adopt': 500, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': 500, 'own_lr_vs_update': 250, 'own_best_vs_adopt': 250, 'own_best_vs_update': 250}.
H1: not evaluable; H2: fail; H3: fail.
Riley et al. (2020): n = 7897 landmarks ≈ 513 patients (p = 38, R²cs 0.042).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6724 | 0.6806 | 0.6783 | 0.6767 | 0.6658 | 0.0080 / 0.0034 / 0.0037 / 0.0037 | 0.28 / 0.00 / 0.48 / 0.48 | {'intercept': 0.96, 'own': 0.04} | -0.54, +0.80, -1.54 | 1853, 205 |
| 500 | 0.6712 | 0.6580 | 0.6617 | 0.6571 | 0.6565 | 0.0110 / 0.0168 / 0.0167 / 0.0170 | 0.32 / 0.00 / 0.08 / 0.04 | {'intercept': 1.0} | -0.02, +2.71, -0.25 | 3737, 415 |
| 1000 | 0.6714 | 0.6452 | 0.6500 | 0.6460 | 0.6535 | 0.0028 / 0.0120 / 0.0272 / 0.0272 | 0.64 / 0.40 / 0.00 / 0.00 | {'intercept': 0.44, 'own': 0.04, 'update': 0.52} | +0.49, +4.33, +0.23 | 7461, 827 |

## O2_nwicu_from_inspire+mimic (external model from inspire + mimic)

Destination: 30,833 landmarks, 2,001 patients, prevalence 0.486.
Regime label: level shift (0.00 of samples with n ≤ 1,000 flagged). Break-even (≥ 80 %): {'own_vs_adopt': None, 'own_vs_update': None, 'own_tuned_vs_adopt': None, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': None, 'own_best_vs_update': None}.
H1: not evaluable; H2: fail; H3: fail.
Riley et al. (2020): n = 4102 landmarks ≈ 267 patients (p = 38, R²cs 0.080).

| n | adopt | update | own | own_tuned | own_lr | regret cv / closed / v1 / v2 | correct cv / closed / v1 / v2 | closed choice | ΔNB own − adopt /100 | events (landmarks, patients) |
|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6530 | 0.6726 | 0.6756 | 0.6723 | 0.6645 | 0.0004 / -0.0000 / 0.0004 / 0.0004 | 0.92 / 0.00 / 0.92 / 0.92 | {'intercept': 0.96, 'logistic': 0.04} | -1.15, -2.48, -1.70 | 1876, 208 |
| 500 | 0.6520 | 0.6577 | 0.6635 | 0.6595 | 0.6587 | 0.0016 / 0.0014 / 0.0015 / 0.0015 | 0.68 / 0.04 / 0.68 / 0.68 | {'intercept': 0.92, 'logistic': 0.04, 'update': 0.04} | -0.53, -0.54, -1.48 | 3748, 414 |
| 1000 | 0.6512 | 0.6454 | 0.6504 | 0.6484 | 0.6532 | 0.0045 / 0.0069 / 0.0068 / 0.0068 | 0.36 / 0.08 / 0.08 / 0.08 | {'intercept': 0.76, 'logistic': 0.16, 'update': 0.08} | -0.03, +1.07, -1.10 | 7476, 828 |

## Confirmatory summary

| hypothesis | units holding | units failing | not evaluable | verdict |
|---|---|---|---|---|
| H1 | 5 | 0 | 4 | holds |
| H2 | 6 | 3 | 0 | fails |
| H3 | 2 | 7 | 0 | fails |
