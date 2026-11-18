# Internal review 8 on `hypo` (post hoc, exploratory)

## hypo_eicu

Break-even (≥ 80 % of samples): {'own_vs_adopt': None, 'own_vs_update': None, 'own_tuned_vs_adopt': None, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': None, 'own_best_vs_update': None}
Riley et al. (2020) for a regression model: n = 1990 landmarks ≈ 137 patients (385 events; p = 46, R²cs 0.186, prevalence 0.193)

| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | ΔNB own − adopt /100 (0.10, 0.20, 0.30) | events (landmarks, patients) |
|---|---|---|---|---|---|---|
| 250 | 0.0004 / 0.0052 / 0.0000 | 0.96 / 0.00 / 1.00 | {'intercept': 0.44, 'keep': 0.52, 'update': 0.04} | +0.0198 (0.00), +0.0152 (0.00), +0.0232 (0.00), +0.0151 (0.00) | -0.53, -0.83, -0.98 | 691, 135 |
| 500 | 0.0001 / 0.0048 / 0.0000 | 0.96 / 0.00 / 1.00 | {'intercept': 0.44, 'keep': 0.4, 'update': 0.16} | +0.0129 (0.00), +0.0087 (0.00), +0.0149 (0.00), +0.0087 (0.00) | -0.31, -0.51, -0.63 | 1426, 275 |
| 1000 | 0.0000 / 0.0005 / 0.0000 | 1.00 / 0.00 / 1.00 | {'intercept': 0.84, 'keep': 0.04, 'logistic': 0.04, 'update': 0.08} | +0.0074 (0.00), +0.0045 (0.00), +0.0116 (0.00), +0.0045 (0.00) | -0.18, -0.30, -0.32 | 2803, 546 |
| 2000 | 0.0003 / 0.0004 / 0.0004 | 0.47 / 0.00 / 0.27 | {'intercept': 0.8666666666666667, 'logistic': 0.13333333333333333} | +0.0033 (0.00), +0.0016 (0.00), +0.0096 (0.00), +0.0016 (0.00) | -0.10, -0.12, -0.12 | 5667, 1103 |
| 4000 | 0.0001 / 0.0011 / 0.0014 | 0.93 / 0.20 / 0.00 | {'intercept': 0.6666666666666666, 'logistic': 0.13333333333333333, 'update': 0.2} | +0.0010 (0.13), +0.0002 (0.47), +0.0085 (0.00), +0.0002 (0.47) | -0.06, -0.02, -0.02 | 11213, 2196 |

## hypo_inspire

Break-even (≥ 80 % of samples): {'own_vs_adopt': 2000, 'own_vs_update': None, 'own_tuned_vs_adopt': 2000, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': 2000, 'own_best_vs_update': None}
Riley et al. (2020) for a regression model: n = 3264 landmarks ≈ 257 patients (429 events; p = 48, R²cs 0.123, prevalence 0.132)

| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | ΔNB own − adopt /100 (0.10, 0.20, 0.30) | events (landmarks, patients) |
|---|---|---|---|---|---|---|
| 250 | 0.0004 / 0.0029 / 0.0004 | 0.72 / 0.00 / 0.72 | {'intercept': 0.24, 'keep': 0.6, 'update': 0.16} | +0.0117 (0.00), +0.0091 (0.00), +0.0149 (0.00), +0.0084 (0.00) | -0.40, -0.55, -0.51 | 396, 92 |
| 500 | 0.0005 / 0.0031 / 0.0006 | 0.60 / 0.08 / 0.52 | {'intercept': 0.36, 'keep': 0.52, 'update': 0.12} | +0.0071 (0.00), +0.0035 (0.08), +0.0120 (0.00), +0.0035 (0.08) | -0.22, -0.29, -0.32 | 845, 195 |
| 1000 | 0.0009 / 0.0024 / 0.0020 | 0.64 / 0.28 / 0.08 | {'intercept': 0.4, 'keep': 0.2, 'logistic': 0.08, 'update': 0.32} | +0.0018 (0.16), -0.0007 (0.56), +0.0090 (0.00), -0.0007 (0.56) | -0.07, -0.09, -0.05 | 1666, 385 |
| 2000 | 0.0002 / 0.0030 / 0.0039 | 0.80 / 0.20 / 0.00 | {'intercept': 0.6666666666666666, 'update': 0.3333333333333333} | -0.0023 (1.00), -0.0034 (1.00), +0.0071 (0.00), -0.0034 (1.00) | +0.08, +0.11, +0.13 | 3405, 776 |
| 4000 | 0.0002 / 0.0004 / 0.0054 | 0.67 / 0.67 / 0.00 | {'logistic': 0.06666666666666667, 'update': 0.9333333333333333} | -0.0049 (1.00), -0.0053 (1.00), +0.0060 (0.00), -0.0054 (1.00) | +0.15, +0.21, +0.20 | 6705, 1542 |

## hypo_mimic

Break-even (≥ 80 % of samples): {'own_vs_adopt': 4000, 'own_vs_update': None, 'own_tuned_vs_adopt': 2000, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': 2000, 'own_best_vs_update': None}
Riley et al. (2020) for a regression model: n = 1685 landmarks ≈ 107 patients (517 events; p = 45, R²cs 0.211, prevalence 0.307)

| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | ΔNB own − adopt /100 (0.10, 0.20, 0.30) | events (landmarks, patients) |
|---|---|---|---|---|---|---|
| 250 | 0.0000 / 0.0076 / 0.0000 | 0.96 / 0.00 / 0.96 | {'intercept': 0.32, 'keep': 0.48, 'logistic': 0.04, 'update': 0.16} | +0.0191 (0.00), +0.0136 (0.00), +0.0165 (0.00), +0.0131 (0.00) | -0.32, -0.54, -1.00 | 1229, 185 |
| 500 | 0.0002 / 0.0013 / 0.0001 | 0.84 / 0.00 / 0.88 | {'intercept': 0.76, 'keep': 0.08, 'logistic': 0.04, 'update': 0.12} | +0.0105 (0.00), +0.0067 (0.00), +0.0106 (0.00), +0.0066 (0.00) | -0.18, -0.24, -0.51 | 2450, 368 |
| 1000 | 0.0007 / 0.0010 / 0.0009 | 0.36 / 0.00 / 0.28 | {'intercept': 0.88, 'logistic': 0.12} | +0.0042 (0.00), +0.0016 (0.08), +0.0068 (0.00), +0.0016 (0.08) | -0.04, -0.04, -0.23 | 4872, 735 |
| 2000 | 0.0000 / 0.0021 / 0.0027 | 1.00 / 0.27 / 0.00 | {'intercept': 0.6666666666666666, 'logistic': 0.06666666666666667, 'update': 0.26666666666666666} | +0.0006 (0.27), -0.0008 (0.80), +0.0050 (0.00), -0.0008 (0.80) | +0.02, +0.08, -0.04 | 9757, 1473 |
| 4000 | 0.0000 / 0.0004 / 0.0046 | 1.00 / 0.93 / 0.00 | {'intercept': 0.06666666666666667, 'update': 0.9333333333333333} | -0.0030 (1.00), -0.0037 (1.00), +0.0041 (0.00), -0.0037 (1.00) | +0.07, +0.17, +0.15 | 19336, 2939 |

## nwicu_inspire

Break-even (≥ 80 % of samples): {'own_vs_adopt': None, 'own_vs_update': None, 'own_tuned_vs_adopt': None, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': None, 'own_best_vs_update': None}
Riley et al. (2020) for a regression model: n = 2196 landmarks ≈ 143 patients (283 events; p = 38, R²cs 0.143, prevalence 0.129)

| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | ΔNB own − adopt /100 (0.10, 0.20, 0.30) | events (landmarks, patients) |
|---|---|---|---|---|---|---|
| 250 | 0.0000 / 0.0064 / 0.0000 | 1.00 / 0.00 / 1.00 | {'intercept': 0.6, 'keep': 0.16, 'logistic': 0.2, 'update': 0.04} | +0.0169 (0.00), +0.0130 (0.00), +0.0098 (0.00), +0.0090 (0.00) | -0.46, -0.74, -0.78 | 512, 110 |
| 500 | 0.0000 / 0.0005 / 0.0000 | 0.92 / 0.00 / 0.92 | {'intercept': 0.68, 'logistic': 0.32} | +0.0126 (0.00), +0.0073 (0.04), +0.0069 (0.00), +0.0056 (0.04) | -0.37, -0.53, -0.63 | 978, 214 |
| 1000 | 0.0001 / 0.0006 / 0.0001 | 0.80 / 0.00 / 0.80 | {'intercept': 0.56, 'logistic': 0.4, 'update': 0.04} | +0.0074 (0.04), +0.0045 (0.08), +0.0049 (0.00), +0.0031 (0.08) | -0.22, -0.30, -0.44 | 1984, 432 |

## nwicu_mimic

Break-even (≥ 80 % of samples): {'own_vs_adopt': None, 'own_vs_update': None, 'own_tuned_vs_adopt': None, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': None, 'own_best_vs_update': None}
Riley et al. (2020) for a regression model: n = 2199 landmarks ≈ 143 patients (283 events; p = 38, R²cs 0.143, prevalence 0.129)

| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | ΔNB own − adopt /100 (0.10, 0.20, 0.30) | events (landmarks, patients) |
|---|---|---|---|---|---|---|
| 250 | 0.0004 / 0.0063 / 0.0000 | 0.92 / 0.00 / 0.96 | {'intercept': 0.36, 'keep': 0.44, 'logistic': 0.04, 'update': 0.16} | +0.0176 (0.00), +0.0133 (0.00), +0.0114 (0.00), +0.0107 (0.00) | -0.41, -0.78, -0.81 | 500, 110 |
| 500 | 0.0002 / 0.0028 / 0.0001 | 0.88 / 0.00 / 0.92 | {'intercept': 0.6, 'keep': 0.16, 'logistic': 0.2, 'update': 0.04} | +0.0115 (0.00), +0.0083 (0.00), +0.0076 (0.00), +0.0062 (0.00) | -0.30, -0.53, -0.48 | 993, 216 |
| 1000 | 0.0004 / 0.0003 / 0.0002 | 0.76 / 0.04 / 0.80 | {'intercept': 0.64, 'logistic': 0.32, 'update': 0.04} | +0.0067 (0.00), +0.0043 (0.00), +0.0045 (0.00), +0.0031 (0.00) | -0.12, -0.26, -0.24 | 1974, 431 |

## nwicu_eicu

Break-even (≥ 80 % of samples): {'own_vs_adopt': None, 'own_vs_update': None, 'own_tuned_vs_adopt': None, 'own_tuned_vs_update': None, 'own_lr_vs_adopt': None, 'own_lr_vs_update': None, 'own_best_vs_adopt': None, 'own_best_vs_update': None}
Riley et al. (2020) for a regression model: n = 2229 landmarks ≈ 145 patients (287 events; p = 38, R²cs 0.141, prevalence 0.129)

| n | regret cv / closed / rule | correct cv / closed / rule | closed choice | own, own_tuned, own_lr, best − adopt | ΔNB own − adopt /100 (0.10, 0.20, 0.30) | events (landmarks, patients) |
|---|---|---|---|---|---|---|
| 250 | 0.0001 / 0.0071 / 0.0001 | 0.96 / 0.00 / 0.96 | {'intercept': 0.8, 'keep': 0.12, 'logistic': 0.08} | +0.0162 (0.00), +0.0128 (0.00), +0.0103 (0.00), +0.0093 (0.00) | -0.52, -0.64, -0.67 | 498, 110 |
| 500 | 0.0003 / 0.0004 / 0.0001 | 0.92 / 0.00 / 0.96 | {'intercept': 0.84, 'logistic': 0.16} | +0.0106 (0.00), +0.0071 (0.08), +0.0063 (0.08), +0.0046 (0.16) | -0.35, -0.39, -0.37 | 997, 216 |
| 1000 | 0.0005 / 0.0008 / 0.0004 | 0.68 / 0.00 / 0.68 | {'intercept': 0.8, 'logistic': 0.2} | +0.0058 (0.04), +0.0028 (0.08), +0.0035 (0.12), +0.0016 (0.20) | -0.22, -0.22, -0.23 | 1988, 434 |

