# Adopt, update or build? and a PRAM replica (post hoc, exploratory; internal review 7)

Log-loss per landmark on each fold's test landmarks; one sample = one draw of n local patients in one fold.

## t2_mimic

Break-even: {'own_vs_adopt': {'first_n_mean': 1000, 'first_n_80pct': 1000}, 'update_vs_adopt': {'first_n_mean': 1000, 'first_n_80pct': 1000}, 'own_vs_update': {'first_n_mean': 1000, 'first_n_80pct': 1000}}
Predictors of own − adopt: {'spearman_slope_vs_gap': -0.009914529914529914, 'spearman_aurocgap_vs_gap': -0.16649572649572647}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 1.0965 | 1.1035 | 1.1292 | 0.00 | 0.80/0.20/0.00 | 0.0073 | 0.0008 | 0.0008 | 0.0078 | 0.0335 | 0.20 |
| 500 | 1.0942 | 1.1188 | 1.1190 | 0.00 | 0.60/0.40/0.00 | 0.0251 | 0.0073 | 0.0039 | 0.0285 | 0.0286 | 0.20 |
| 1000 | 1.0923 | 1.0705 | 1.0593 | 1.00 | 0.00/0.00/1.00 | 0.0014 | 0.0112 | 0.0330 | 0.0112 | 0.0000 | 0.80 |
| 2000 | 1.0921 | 1.0513 | 1.0388 | 1.00 | 0.00/0.00/1.00 | 0.0000 | 0.0279 | 0.0533 | 0.0125 | 0.0000 | 1.00 |
| 4000 | 1.0919 | 1.0392 | 1.0222 | 1.00 | 0.00/0.00/1.00 | 0.0000 | 0.0169 | 0.0697 | 0.0169 | 0.0000 | 1.00 |
| 8000 | 1.0918 | 1.0188 | 1.0025 | 1.00 | 0.00/0.00/1.00 | 0.0000 | 0.0163 | 0.0893 | 0.0163 | 0.0000 | 1.00 |

## t2_eicu

Break-even: {'own_vs_adopt': {'first_n_mean': 500, 'first_n_80pct': 500}, 'update_vs_adopt': {'first_n_mean': 1000, 'first_n_80pct': 1000}, 'own_vs_update': {'first_n_mean': 250, 'first_n_80pct': 250}}
Predictors of own − adopt: {'spearman_slope_vs_gap': 0.1835897435897436, 'spearman_aurocgap_vs_gap': -0.1268376068376068}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 1.1103 | 1.1455 | 1.1216 | 0.00 | 1.00/0.00/0.00 | 0.0000 | 0.0000 | 0.0000 | 0.0352 | 0.0113 | 1.00 |
| 500 | 1.1099 | 1.1303 | 1.1024 | 0.80 | 0.20/0.00/0.80 | 0.0113 | 0.0317 | 0.0113 | 0.0317 | 0.0037 | 0.20 |
| 1000 | 1.1048 | 1.0913 | 1.0731 | 1.00 | 0.00/0.00/1.00 | 0.0000 | 0.0182 | 0.0317 | 0.0182 | 0.0000 | 1.00 |
| 2000 | 1.1034 | 1.0718 | 1.0544 | 1.00 | 0.00/0.00/1.00 | 0.0000 | 0.0174 | 0.0491 | 0.0174 | 0.0000 | 1.00 |
| 4000 | 1.1034 | 1.0484 | 1.0353 | 1.00 | 0.00/0.00/1.00 | 0.0000 | 0.0132 | 0.0682 | 0.0132 | 0.0000 | 1.00 |
| 8000 | 1.1036 | 1.0331 | 1.0266 | 1.00 | 0.00/0.00/1.00 | 0.0000 | 0.0065 | 0.0769 | 0.0065 | 0.0000 | 1.00 |

