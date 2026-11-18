# Adopt, update or build? and a PRAM replica (post hoc, exploratory; internal review 7)

Log-loss per landmark on each fold's test landmarks; one sample = one draw of n local patients in one fold.

## hypo_eicu

Break-even: {'own_vs_adopt': {'first_n_mean': None, 'first_n_80pct': None}, 'update_vs_adopt': {'first_n_mean': 2000, 'first_n_80pct': 4000}, 'own_vs_update': {'first_n_mean': None, 'first_n_80pct': None}}
Predictors of own − adopt: {'spearman_slope_vs_gap': 0.08799502384408044, 'spearman_aurocgap_vs_gap': -0.0798465685258138}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3891 | 0.3950 | 0.4089 | 0.00 | 1.00/0.00/0.00 | 0.0004 | 0.0000 | 0.0000 | 0.0060 | 0.0198 | 0.96 |
| 500 | 0.3887 | 0.3928 | 0.4016 | 0.00 | 1.00/0.00/0.00 | 0.0001 | 0.0000 | 0.0000 | 0.0041 | 0.0129 | 0.96 |
| 1000 | 0.3885 | 0.3904 | 0.3959 | 0.00 | 1.00/0.00/0.00 | 0.0000 | 0.0000 | 0.0000 | 0.0019 | 0.0074 | 1.00 |
| 2000 | 0.3885 | 0.3882 | 0.3918 | 0.00 | 0.27/0.73/0.00 | 0.0003 | 0.0004 | 0.0004 | 0.0001 | 0.0037 | 0.47 |
| 4000 | 0.3884 | 0.3870 | 0.3893 | 0.13 | 0.00/1.00/0.00 | 0.0001 | 0.0014 | 0.0014 | 0.0000 | 0.0023 | 0.93 |

PRAM replica (Δ log-loss mean, share of samples with a lower log-loss):

- n = 250: pram_lr_vs_lr_base -0.0018 (0.64); pram_lr_vs_lr_logistic +0.0066 (0.00); pram_lr_iso_vs_lr_logistic +0.0421 (0.00); pram_lgbm_vs_lgbm_base -0.0011 (0.52); pram_lgbm_vs_adopt +0.0084 (0.00); pram_lgbm_iso_vs_adopt +0.0445 (0.00); pram_lr_iso_vs_own +0.0326 (0.00); pram_lgbm_iso_vs_own +0.0247 (0.12); α {'lgbm': 0.18, 'lr': 0.19200000000000003}
- n = 500: pram_lr_vs_lr_base -0.0032 (0.84); pram_lr_vs_lr_logistic +0.0055 (0.00); pram_lr_iso_vs_lr_logistic +0.0269 (0.00); pram_lgbm_vs_lgbm_base -0.0023 (0.84); pram_lgbm_vs_adopt +0.0077 (0.00); pram_lgbm_iso_vs_adopt +0.0253 (0.00); pram_lr_iso_vs_own +0.0243 (0.08); pram_lgbm_iso_vs_own +0.0125 (0.12); α {'lgbm': 0.172, 'lr': 0.22799999999999998}
- n = 1000: pram_lr_vs_lr_base -0.0046 (1.00); pram_lr_vs_lr_logistic +0.0044 (0.00); pram_lr_iso_vs_lr_logistic +0.0102 (0.04); pram_lgbm_vs_lgbm_base -0.0032 (1.00); pram_lgbm_vs_adopt +0.0070 (0.00); pram_lgbm_iso_vs_adopt +0.0137 (0.00); pram_lr_iso_vs_own +0.0130 (0.00); pram_lgbm_iso_vs_own +0.0063 (0.12); α {'lgbm': 0.30400000000000005, 'lr': 0.36800000000000005}
- n = 2000: pram_lr_vs_lr_base -0.0057 (1.00); pram_lr_vs_lr_logistic +0.0034 (0.00); pram_lr_iso_vs_lr_logistic +0.0040 (0.13); pram_lgbm_vs_lgbm_base -0.0036 (1.00); pram_lgbm_vs_adopt +0.0066 (0.00); pram_lgbm_iso_vs_adopt +0.0068 (0.00); pram_lr_iso_vs_own +0.0109 (0.00); pram_lgbm_iso_vs_own +0.0035 (0.07); α {'lgbm': 0.30666666666666664, 'lr': 0.3866666666666667}
- n = 4000: pram_lr_vs_lr_base -0.0070 (1.00); pram_lr_vs_lr_logistic +0.0022 (0.00); pram_lr_iso_vs_lr_logistic +0.0002 (0.53); pram_lgbm_vs_lgbm_base -0.0044 (1.00); pram_lgbm_vs_adopt +0.0058 (0.00); pram_lgbm_iso_vs_adopt +0.0046 (0.00); pram_lr_iso_vs_own +0.0094 (0.00); pram_lgbm_iso_vs_own +0.0036 (0.00); α {'lgbm': 0.33999999999999997, 'lr': 0.46}

## hypo_inspire

Break-even: {'own_vs_adopt': {'first_n_mean': 2000, 'first_n_80pct': 2000}, 'update_vs_adopt': {'first_n_mean': 1000, 'first_n_80pct': 1000}, 'own_vs_update': {'first_n_mean': None, 'first_n_80pct': None}}
Predictors of own − adopt: {'spearman_slope_vs_gap': 0.0467343976777939, 'spearman_aurocgap_vs_gap': -0.01895086046029442}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3249 | 0.3261 | 0.3366 | 0.00 | 0.72/0.28/0.00 | 0.0004 | 0.0004 | 0.0004 | 0.0016 | 0.0121 | 0.72 |
| 500 | 0.3241 | 0.3243 | 0.3313 | 0.00 | 0.52/0.48/0.00 | 0.0005 | 0.0006 | 0.0006 | 0.0007 | 0.0077 | 0.60 |
| 1000 | 0.3239 | 0.3220 | 0.3258 | 0.16 | 0.04/0.92/0.04 | 0.0009 | 0.0020 | 0.0021 | 0.0001 | 0.0039 | 0.64 |
| 2000 | 0.3238 | 0.3201 | 0.3215 | 1.00 | 0.00/0.80/0.20 | 0.0002 | 0.0039 | 0.0039 | 0.0002 | 0.0016 | 0.80 |
| 4000 | 0.3237 | 0.3185 | 0.3188 | 1.00 | 0.00/0.67/0.33 | 0.0002 | 0.0054 | 0.0054 | 0.0002 | 0.0005 | 0.67 |

PRAM replica (Δ log-loss mean, share of samples with a lower log-loss):

- n = 250: pram_lr_vs_lr_base -0.0062 (0.96); pram_lr_vs_lr_logistic -0.0024 (0.80); pram_lr_iso_vs_lr_logistic +0.0459 (0.00); pram_lgbm_vs_lgbm_base -0.0023 (0.80); pram_lgbm_vs_adopt +0.0015 (0.20); pram_lgbm_iso_vs_adopt +0.0493 (0.00); pram_lr_iso_vs_own +0.0440 (0.00); pram_lgbm_iso_vs_own +0.0376 (0.04); α {'lgbm': 0.26, 'lr': 0.27599999999999997}
- n = 500: pram_lr_vs_lr_base -0.0085 (1.00); pram_lr_vs_lr_logistic -0.0034 (1.00); pram_lr_iso_vs_lr_logistic +0.0191 (0.12); pram_lgbm_vs_lgbm_base -0.0031 (0.96); pram_lgbm_vs_adopt +0.0016 (0.08); pram_lgbm_iso_vs_adopt +0.0230 (0.00); pram_lr_iso_vs_own +0.0212 (0.12); pram_lgbm_iso_vs_own +0.0159 (0.20); α {'lgbm': 0.32400000000000007, 'lr': 0.38400000000000006}
- n = 1000: pram_lr_vs_lr_base -0.0093 (1.00); pram_lr_vs_lr_logistic -0.0040 (1.00); pram_lr_iso_vs_lr_logistic +0.0076 (0.20); pram_lgbm_vs_lgbm_base -0.0036 (1.00); pram_lgbm_vs_adopt +0.0012 (0.08); pram_lgbm_iso_vs_adopt +0.0133 (0.00); pram_lr_iso_vs_own +0.0150 (0.00); pram_lgbm_iso_vs_own +0.0114 (0.04); α {'lgbm': 0.37200000000000005, 'lr': 0.43200000000000005}
- n = 2000: pram_lr_vs_lr_base -0.0098 (1.00); pram_lr_vs_lr_logistic -0.0044 (1.00); pram_lr_iso_vs_lr_logistic +0.0008 (0.53); pram_lgbm_vs_lgbm_base -0.0043 (1.00); pram_lgbm_vs_adopt +0.0007 (0.13); pram_lgbm_iso_vs_adopt +0.0065 (0.00); pram_lr_iso_vs_own +0.0123 (0.00); pram_lgbm_iso_vs_own +0.0088 (0.00); α {'lgbm': 0.4, 'lr': 0.46666666666666673}
- n = 4000: pram_lr_vs_lr_base -0.0108 (1.00); pram_lr_vs_lr_logistic -0.0053 (1.00); pram_lr_iso_vs_lr_logistic -0.0037 (0.87); pram_lgbm_vs_lgbm_base -0.0050 (1.00); pram_lgbm_vs_adopt +0.0001 (0.27); pram_lgbm_iso_vs_adopt +0.0016 (0.20); pram_lr_iso_vs_own +0.0104 (0.00); pram_lgbm_iso_vs_own +0.0065 (0.00); α {'lgbm': 0.4133333333333334, 'lr': 0.4866666666666667}

## hypo_mimic

Break-even: {'own_vs_adopt': {'first_n_mean': 4000, 'first_n_80pct': 4000}, 'update_vs_adopt': {'first_n_mean': 1000, 'first_n_80pct': 2000}, 'own_vs_update': {'first_n_mean': None, 'first_n_80pct': None}}
Predictors of own − adopt: {'spearman_slope_vs_gap': -0.09232842629069044, 'spearman_aurocgap_vs_gap': 0.09782293178519592}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.4986 | 0.5045 | 0.5176 | 0.00 | 0.96/0.04/0.00 | 0.0000 | 0.0000 | 0.0000 | 0.0060 | 0.0191 | 0.96 |
| 500 | 0.4982 | 0.5007 | 0.5088 | 0.00 | 0.92/0.08/0.00 | 0.0002 | 0.0001 | 0.0000 | 0.0025 | 0.0106 | 0.84 |
| 1000 | 0.4980 | 0.4972 | 0.5022 | 0.00 | 0.28/0.72/0.00 | 0.0007 | 0.0009 | 0.0009 | 0.0002 | 0.0051 | 0.36 |
| 2000 | 0.4979 | 0.4952 | 0.4985 | 0.27 | 0.00/1.00/0.00 | 0.0000 | 0.0027 | 0.0027 | 0.0000 | 0.0033 | 1.00 |
| 4000 | 0.4979 | 0.4933 | 0.4949 | 1.00 | 0.00/1.00/0.00 | 0.0000 | 0.0046 | 0.0046 | 0.0000 | 0.0016 | 1.00 |

PRAM replica (Δ log-loss mean, share of samples with a lower log-loss):

- n = 250: pram_lr_vs_lr_base -0.0020 (0.72); pram_lr_vs_lr_logistic +0.0072 (0.00); pram_lr_iso_vs_lr_logistic +0.0316 (0.00); pram_lgbm_vs_lgbm_base -0.0030 (0.80); pram_lgbm_vs_adopt +0.0092 (0.00); pram_lgbm_iso_vs_adopt +0.0496 (0.00); pram_lr_iso_vs_own +0.0222 (0.20); pram_lgbm_iso_vs_own +0.0305 (0.28); α {'lgbm': 0.15600000000000003, 'lr': 0.14800000000000002}
- n = 500: pram_lr_vs_lr_base -0.0033 (0.84); pram_lr_vs_lr_logistic +0.0062 (0.00); pram_lr_iso_vs_lr_logistic +0.0194 (0.04); pram_lgbm_vs_lgbm_base -0.0047 (0.96); pram_lgbm_vs_adopt +0.0078 (0.00); pram_lgbm_iso_vs_adopt +0.0219 (0.00); pram_lr_iso_vs_own +0.0186 (0.08); pram_lgbm_iso_vs_own +0.0114 (0.20); α {'lgbm': 0.2, 'lr': 0.17200000000000004}
- n = 1000: pram_lr_vs_lr_base -0.0047 (1.00); pram_lr_vs_lr_logistic +0.0051 (0.00); pram_lr_iso_vs_lr_logistic +0.0057 (0.20); pram_lgbm_vs_lgbm_base -0.0058 (1.00); pram_lgbm_vs_adopt +0.0069 (0.00); pram_lgbm_iso_vs_adopt +0.0109 (0.00); pram_lr_iso_vs_own +0.0112 (0.00); pram_lgbm_iso_vs_own +0.0067 (0.16); α {'lgbm': 0.23600000000000002, 'lr': 0.22}
- n = 2000: pram_lr_vs_lr_base -0.0059 (1.00); pram_lr_vs_lr_logistic +0.0040 (0.00); pram_lr_iso_vs_lr_logistic +0.0020 (0.33); pram_lgbm_vs_lgbm_base -0.0068 (1.00); pram_lgbm_vs_adopt +0.0059 (0.00); pram_lgbm_iso_vs_adopt +0.0045 (0.00); pram_lr_iso_vs_own +0.0111 (0.00); pram_lgbm_iso_vs_own +0.0039 (0.13); α {'lgbm': 0.27999999999999997, 'lr': 0.2733333333333333}
- n = 4000: pram_lr_vs_lr_base -0.0070 (1.00); pram_lr_vs_lr_logistic +0.0029 (0.00); pram_lr_iso_vs_lr_logistic -0.0012 (0.80); pram_lgbm_vs_lgbm_base -0.0076 (1.00); pram_lgbm_vs_adopt +0.0052 (0.00); pram_lgbm_iso_vs_adopt +0.0013 (0.33); pram_lr_iso_vs_own +0.0115 (0.00); pram_lgbm_iso_vs_own +0.0043 (0.00); α {'lgbm': 0.2933333333333332, 'lr': 0.29999999999999993}

## nwicu_inspire

Break-even: {'own_vs_adopt': {'first_n_mean': None, 'first_n_80pct': None}, 'update_vs_adopt': {'first_n_mean': None, 'first_n_80pct': None}, 'own_vs_update': {'first_n_mean': None, 'first_n_80pct': None}}
Predictors of own − adopt: {'spearman_slope_vs_gap': -0.22341394025604552, 'spearman_aurocgap_vs_gap': 0.22108108108108104}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3069 | 0.3151 | 0.3238 | 0.00 | 1.00/0.00/0.00 | 0.0000 | 0.0000 | 0.0000 | 0.0082 | 0.0169 | 1.00 |
| 500 | 0.3070 | 0.3121 | 0.3196 | 0.00 | 0.92/0.08/0.00 | 0.0000 | 0.0000 | 0.0000 | 0.0051 | 0.0126 | 0.92 |
| 1000 | 0.3066 | 0.3096 | 0.3141 | 0.04 | 0.80/0.16/0.04 | 0.0001 | 0.0001 | 0.0001 | 0.0031 | 0.0076 | 0.80 |

PRAM replica (Δ log-loss mean, share of samples with a lower log-loss):

- n = 250: pram_lr_vs_lr_base -0.0290 (0.96); pram_lr_vs_lr_logistic +0.0140 (0.00); pram_lr_iso_vs_lr_logistic +0.0413 (0.00); pram_lgbm_vs_lgbm_base -0.0215 (1.00); pram_lgbm_vs_adopt +0.0156 (0.00); pram_lgbm_iso_vs_adopt +0.0538 (0.00); pram_lr_iso_vs_own +0.0306 (0.04); pram_lgbm_iso_vs_own +0.0369 (0.08); α {'lgbm': 0.5760000000000001, 'lr': 0.6359999999999999}
- n = 500: pram_lr_vs_lr_base -0.0307 (1.00); pram_lr_vs_lr_logistic +0.0122 (0.00); pram_lr_iso_vs_lr_logistic +0.0251 (0.00); pram_lgbm_vs_lgbm_base -0.0234 (1.00); pram_lgbm_vs_adopt +0.0136 (0.00); pram_lgbm_iso_vs_adopt +0.0252 (0.00); pram_lr_iso_vs_own +0.0188 (0.08); pram_lgbm_iso_vs_own +0.0127 (0.24); α {'lgbm': 0.62, 'lr': 0.684}
- n = 1000: pram_lr_vs_lr_base -0.0346 (1.00); pram_lr_vs_lr_logistic +0.0086 (0.00); pram_lr_iso_vs_lr_logistic +0.0118 (0.00); pram_lgbm_vs_lgbm_base -0.0261 (1.00); pram_lgbm_vs_adopt +0.0112 (0.00); pram_lgbm_iso_vs_adopt +0.0147 (0.00); pram_lr_iso_vs_own +0.0107 (0.12); pram_lgbm_iso_vs_own +0.0073 (0.12); α {'lgbm': 0.648, 'lr': 0.7200000000000002}

## nwicu_mimic

Break-even: {'own_vs_adopt': {'first_n_mean': None, 'first_n_80pct': None}, 'update_vs_adopt': {'first_n_mean': None, 'first_n_80pct': None}, 'own_vs_update': {'first_n_mean': None, 'first_n_80pct': None}}
Predictors of own − adopt: {'spearman_slope_vs_gap': -0.12688477951635846, 'spearman_aurocgap_vs_gap': 0.16273115220483642}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3069 | 0.3120 | 0.3245 | 0.00 | 0.96/0.04/0.00 | 0.0004 | 0.0000 | 0.0000 | 0.0051 | 0.0176 | 0.92 |
| 500 | 0.3068 | 0.3104 | 0.3184 | 0.00 | 0.92/0.08/0.00 | 0.0002 | 0.0001 | 0.0001 | 0.0037 | 0.0116 | 0.88 |
| 1000 | 0.3067 | 0.3081 | 0.3133 | 0.00 | 0.80/0.20/0.00 | 0.0004 | 0.0002 | 0.0002 | 0.0016 | 0.0068 | 0.76 |

PRAM replica (Δ log-loss mean, share of samples with a lower log-loss):

- n = 250: pram_lr_vs_lr_base -0.0055 (0.88); pram_lr_vs_lr_logistic +0.0125 (0.00); pram_lr_iso_vs_lr_logistic +0.0446 (0.00); pram_lgbm_vs_lgbm_base -0.0025 (0.76); pram_lgbm_vs_adopt +0.0092 (0.00); pram_lgbm_iso_vs_adopt +0.0405 (0.00); pram_lr_iso_vs_own +0.0332 (0.04); pram_lgbm_iso_vs_own +0.0229 (0.24); α {'lgbm': 0.3, 'lr': 0.38}
- n = 500: pram_lr_vs_lr_base -0.0089 (1.00); pram_lr_vs_lr_logistic +0.0093 (0.00); pram_lr_iso_vs_lr_logistic +0.0223 (0.08); pram_lgbm_vs_lgbm_base -0.0045 (1.00); pram_lgbm_vs_adopt +0.0073 (0.00); pram_lgbm_iso_vs_adopt +0.0196 (0.00); pram_lr_iso_vs_own +0.0170 (0.20); pram_lgbm_iso_vs_own +0.0081 (0.36); α {'lgbm': 0.32, 'lr': 0.456}
- n = 1000: pram_lr_vs_lr_base -0.0112 (1.00); pram_lr_vs_lr_logistic +0.0072 (0.00); pram_lr_iso_vs_lr_logistic +0.0087 (0.20); pram_lgbm_vs_lgbm_base -0.0062 (1.00); pram_lgbm_vs_adopt +0.0058 (0.00); pram_lgbm_iso_vs_adopt +0.0085 (0.12); pram_lr_iso_vs_own +0.0082 (0.12); pram_lgbm_iso_vs_own +0.0018 (0.56); α {'lgbm': 0.40800000000000003, 'lr': 0.548}

## nwicu_eicu

Break-even: {'own_vs_adopt': {'first_n_mean': None, 'first_n_80pct': None}, 'update_vs_adopt': {'first_n_mean': None, 'first_n_80pct': None}, 'own_vs_update': {'first_n_mean': None, 'first_n_80pct': None}}
Predictors of own − adopt: {'spearman_slope_vs_gap': -0.1813371266002845, 'spearman_aurocgap_vs_gap': 0.23149359886201992}

| n | adopt | update | own | own<adopt (share) | best: adopt/update/own | regret cv | regret rule | regret always-adopt | always-update | always-own | cv correct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3082 | 0.3167 | 0.3244 | 0.00 | 0.96/0.04/0.00 | 0.0001 | 0.0001 | 0.0001 | 0.0086 | 0.0163 | 0.96 |
| 500 | 0.3079 | 0.3125 | 0.3185 | 0.00 | 0.96/0.04/0.00 | 0.0003 | 0.0001 | 0.0001 | 0.0047 | 0.0107 | 0.92 |
| 1000 | 0.3077 | 0.3090 | 0.3135 | 0.04 | 0.68/0.32/0.00 | 0.0005 | 0.0004 | 0.0004 | 0.0017 | 0.0062 | 0.68 |

PRAM replica (Δ log-loss mean, share of samples with a lower log-loss):

- n = 250: pram_lr_vs_lr_base -0.0416 (1.00); pram_lr_vs_lr_logistic +0.0153 (0.00); pram_lr_iso_vs_lr_logistic +0.0462 (0.00); pram_lgbm_vs_lgbm_base -0.0296 (1.00); pram_lgbm_vs_adopt +0.0159 (0.00); pram_lgbm_iso_vs_adopt +0.0488 (0.00); pram_lr_iso_vs_own +0.0363 (0.08); pram_lgbm_iso_vs_own +0.0326 (0.20); α {'lgbm': 0.608, 'lr': 0.688}
- n = 500: pram_lr_vs_lr_base -0.0444 (1.00); pram_lr_vs_lr_logistic +0.0128 (0.00); pram_lr_iso_vs_lr_logistic +0.0313 (0.00); pram_lgbm_vs_lgbm_base -0.0314 (1.00); pram_lgbm_vs_adopt +0.0143 (0.00); pram_lgbm_iso_vs_adopt +0.0289 (0.00); pram_lr_iso_vs_own +0.0271 (0.00); pram_lgbm_iso_vs_own +0.0183 (0.12); α {'lgbm': 0.676, 'lr': 0.7760000000000001}
- n = 1000: pram_lr_vs_lr_base -0.0492 (1.00); pram_lr_vs_lr_logistic +0.0082 (0.00); pram_lr_iso_vs_lr_logistic +0.0136 (0.00); pram_lgbm_vs_lgbm_base -0.0351 (1.00); pram_lgbm_vs_adopt +0.0109 (0.00); pram_lgbm_iso_vs_adopt +0.0153 (0.00); pram_lr_iso_vs_own +0.0142 (0.04); pram_lgbm_iso_vs_own +0.0095 (0.12); α {'lgbm': 0.684, 'lr': 0.76}

