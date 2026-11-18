# Phase 2: update before you build under realistic conditions (pre-registered, OSF 10.17605/OSF.IO/SAJEX)

Log-loss per landmark on held-out landmarks; samples of n local patients. 'Beats' = lower log-loss in ≥ 80 % of the samples. Best external = adopt, update or update_tuned; best own = build, build_tuned or build_lr.

## Hypotheses

```
{
 "G1": {
  "units": 33,
  "exceptions": [],
  "verdict": "holds"
 },
 "G2": {
  "estimate": {
   "rd": 0.3733279559050884,
   "sens": 0.5273972602739726,
   "spec": 0.8263950398582817,
   "ppv": 0.5789473684210527,
   "npv": 0.7943805874840357,
   "flagged": 931,
   "own_wins": 1022,
   "samples": 3280
  },
  "ci95": {
   "rd": [
    0.2284391304355089,
    0.5061156494000933
   ],
   "sens": [
    0.3777283273279971,
    0.65708264561361
   ],
   "spec": [
    0.7538194287522032,
    0.8887925356569276
   ],
   "ppv": [
    0.44490535621120014,
    0.7004622838774108
   ],
   "npv": [
    0.7274690473238913,
    0.8552975414467104
   ]
  },
  "holds": true,
  "verdict": "holds"
 },
 "G3": {
  "trend": {
   "z": 16.67823851150784,
   "p_one_sided": 0.0
  },
  "own_beats_ext_share_by_level": {
   "M0": 0.24166666666666667,
   "M1": 0.8083333333333333,
   "M2": 0.9041666666666667,
   "M3": 0.8958333333333334
  },
  "m3_n4000_build_beats_update": [
   "M_hypo_inspire",
   "M_hypo_mimic",
   "M_hypo_eicu",
   "M_O1_mimic",
   "M_O1_eicu",
   "M_O2_inspire",
   "M_O2_mimic",
   "M_O2_eicu"
  ],
  "units_reaching_4000": 8,
  "a": true,
  "b": true,
  "verdict": "holds"
 },
 "G4": {
  "cells": 73,
  "cv_median": 9.286285324986293e-05,
  "cv_p90": 0.0010847230441463451,
  "cv_le_closed_share": 0.9041095890410958,
  "verdict": "holds"
 }
}
```

## H_hypo_h73

1,680 patients, 28,164 landmarks, prevalence 0.146. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.3190 | 0.3251 | 0.3395 | 0.3237 | 0.3374 | 0.3487 | +0.0171 (0.00) | 0.0002 / 0.0076 / 0.0002 | 0.08 |
| 250 | 0.3172 | 0.3196 | 0.3286 | 0.3179 | 0.3245 | 0.3272 | +0.0070 (0.00) | 0.0006 / 0.0058 / 0.0000 | 0.00 |
| 500 | 0.3172 | 0.3164 | 0.3231 | 0.3150 | 0.3197 | 0.3224 | +0.0048 (0.00) | 0.0010 / 0.0021 / 0.0012 | 0.00 |

## H_hypo_h413

1,102 patients, 13,625 landmarks, prevalence 0.200. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4125 | 0.4150 | 0.4340 | 0.4154 | 0.4305 | 0.4442 | +0.0179 (0.00) | 0.0027 / 0.0034 / 0.0011 | 0.32 |
| 250 | 0.4110 | 0.4117 | 0.4214 | 0.4102 | 0.4174 | 0.4307 | +0.0082 (0.04) | 0.0018 / 0.0038 / 0.0011 | 0.16 |
| 500 | 0.4107 | 0.4093 | 0.4147 | 0.4080 | 0.4119 | 0.4227 | +0.0040 (0.08) | 0.0015 / 0.0031 / 0.0021 | 0.04 |

## H_hypo_h167

941 patients, 12,157 landmarks, prevalence 0.215. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4150 | 0.4199 | 0.4372 | 0.4210 | 0.4345 | 0.4523 | +0.0194 (0.00) | 0.0014 / 0.0052 / 0.0007 | 0.36 |
| 250 | 0.4135 | 0.4184 | 0.4296 | 0.4177 | 0.4255 | 0.4357 | +0.0124 (0.00) | 0.0019 / 0.0053 / 0.0009 | 0.12 |
| 500 | 0.4131 | 0.4166 | 0.4237 | 0.4150 | 0.4191 | 0.4314 | +0.0068 (0.00) | 0.0010 / 0.0027 / 0.0007 | 0.00 |

## H_hypo_h243

818 patients, 13,631 landmarks, prevalence 0.230. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': 500, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4477 | 0.4488 | 0.4674 | 0.4473 | 0.4629 | 0.4751 | +0.0171 (0.00) | 0.0020 / 0.0057 / 0.0017 | 0.60 |
| 250 | 0.4457 | 0.4439 | 0.4559 | 0.4413 | 0.4518 | 0.4575 | +0.0096 (0.04) | 0.0015 / 0.0071 / 0.0023 | 0.44 |
| 500 | 0.4455 | 0.4417 | 0.4488 | 0.4396 | 0.4458 | 0.4521 | +0.0059 (0.12) | 0.0021 / 0.0054 / 0.0041 | 0.32 |

## H_hypo_h420

772 patients, 12,277 landmarks, prevalence 0.251. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4266 | 0.4300 | 0.4518 | 0.4297 | 0.4468 | 0.4579 | +0.0204 (0.00) | 0.0048 / 0.0031 / 0.0009 | 0.08 |
| 250 | 0.4254 | 0.4264 | 0.4406 | 0.4259 | 0.4358 | 0.4444 | +0.0118 (0.00) | 0.0020 / 0.0040 / 0.0014 | 0.00 |
| 500 | 0.4254 | 0.4246 | 0.4339 | 0.4239 | 0.4298 | 0.4378 | +0.0067 (0.00) | 0.0029 / 0.0028 / 0.0021 | 0.00 |

## H_hypo_h458

743 patients, 11,629 landmarks, prevalence 0.136. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.3242 | 0.3309 | 0.3452 | 0.3315 | 0.3405 | 0.3518 | +0.0158 (0.04) | 0.0007 / 0.0136 / 0.0001 | 0.08 |
| 250 | 0.3234 | 0.3300 | 0.3397 | 0.3274 | 0.3344 | 0.3430 | +0.0108 (0.00) | 0.0006 / 0.0045 / 0.0000 | 0.00 |
| 500 | 0.3232 | 0.3267 | 0.3334 | 0.3242 | 0.3281 | 0.3365 | +0.0062 (0.08) | 0.0009 / 0.0001 / 0.0004 | 0.00 |

## H_hypo_h338

729 patients, 10,864 landmarks, prevalence 0.215. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4259 | 0.4330 | 0.4503 | 0.4309 | 0.4467 | 0.4587 | +0.0204 (0.00) | 0.0013 / 0.0096 / 0.0001 | 0.12 |
| 250 | 0.4255 | 0.4285 | 0.4394 | 0.4254 | 0.4344 | 0.4456 | +0.0103 (0.00) | 0.0003 / 0.0051 / 0.0003 | 0.00 |
| 500 | 0.4249 | 0.4268 | 0.4341 | 0.4247 | 0.4302 | 0.4369 | +0.0062 (0.00) | 0.0003 / 0.0033 / 0.0003 | 0.00 |

## H_hypo_h252

711 patients, 11,559 landmarks, prevalence 0.168. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.3649 | 0.3694 | 0.3818 | 0.3669 | 0.3775 | 0.3901 | +0.0134 (0.00) | 0.0008 / 0.0130 / 0.0008 | 0.00 |
| 250 | 0.3640 | 0.3668 | 0.3762 | 0.3640 | 0.3719 | 0.3764 | +0.0090 (0.00) | 0.0020 / 0.0072 / 0.0010 | 0.00 |
| 500 | 0.3636 | 0.3617 | 0.3668 | 0.3601 | 0.3642 | 0.3703 | +0.0042 (0.20) | 0.0031 / 0.0037 / 0.0029 | 0.00 |

## H_hypo_h443

699 patients, 11,184 landmarks, prevalence 0.169. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.3613 | 0.3637 | 0.3791 | 0.3634 | 0.3760 | 0.3927 | +0.0144 (0.00) | 0.0014 / 0.0031 / 0.0001 | 0.04 |
| 250 | 0.3604 | 0.3610 | 0.3700 | 0.3597 | 0.3663 | 0.3797 | +0.0073 (0.04) | 0.0017 / 0.0034 / 0.0009 | 0.00 |
| 500 | 0.3600 | 0.3583 | 0.3658 | 0.3578 | 0.3627 | 0.3755 | +0.0053 (0.08) | 0.0019 / 0.0027 / 0.0023 | 0.00 |

## H_hypo_h300

663 patients, 9,323 landmarks, prevalence 0.226. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4365 | 0.4391 | 0.4570 | 0.4389 | 0.4527 | 0.4687 | +0.0168 (0.00) | 0.0013 / 0.0044 / 0.0006 | 0.28 |
| 250 | 0.4357 | 0.4375 | 0.4490 | 0.4362 | 0.4442 | 0.4534 | +0.0091 (0.04) | 0.0010 / 0.0037 / 0.0006 | 0.32 |
| 500 | 0.4354 | 0.4356 | 0.4427 | 0.4342 | 0.4387 | 0.4464 | +0.0053 (0.04) | 0.0013 / 0.0040 / 0.0009 | 0.20 |

## H_hypo_h152

661 patients, 8,125 landmarks, prevalence 0.245. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4548 | 0.4604 | 0.4793 | 0.4601 | 0.4758 | 0.4938 | +0.0211 (0.00) | 0.0020 / 0.0099 / 0.0000 | 0.12 |
| 250 | 0.4544 | 0.4572 | 0.4678 | 0.4545 | 0.4639 | 0.4814 | +0.0107 (0.00) | 0.0017 / 0.0046 / 0.0009 | 0.00 |
| 500 | 0.4541 | 0.4536 | 0.4611 | 0.4519 | 0.4590 | 0.4743 | +0.0066 (0.12) | 0.0014 / 0.0027 / 0.0014 | 0.00 |

## H_hypo_h411

651 patients, 7,941 landmarks, prevalence 0.257. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4603 | 0.4631 | 0.4876 | 0.4621 | 0.4841 | 0.4940 | +0.0229 (0.00) | 0.0048 / 0.0027 / 0.0018 | 0.40 |
| 250 | 0.4593 | 0.4593 | 0.4739 | 0.4595 | 0.4693 | 0.4760 | +0.0113 (0.08) | 0.0028 / 0.0021 / 0.0019 | 0.48 |
| 500 | 0.4583 | 0.4570 | 0.4651 | 0.4569 | 0.4611 | 0.4690 | +0.0048 (0.24) | 0.0019 / 0.0036 / 0.0021 | 0.20 |

## H_hypo_h264

650 patients, 10,001 landmarks, prevalence 0.185. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.3705 | 0.3714 | 0.3934 | 0.3716 | 0.3908 | 0.4024 | +0.0203 (0.00) | 0.0019 / 0.0011 / 0.0010 | 0.00 |
| 250 | 0.3692 | 0.3705 | 0.3894 | 0.3699 | 0.3828 | 0.3882 | +0.0133 (0.00) | 0.0005 / 0.0015 / 0.0003 | 0.00 |
| 500 | 0.3691 | 0.3699 | 0.3827 | 0.3689 | 0.3765 | 0.3801 | +0.0082 (0.00) | 0.0006 / 0.0018 / 0.0005 | 0.00 |

## H_hypo_h449

647 patients, 9,372 landmarks, prevalence 0.121. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.2801 | 0.2881 | 0.3055 | 0.2868 | 0.3033 | 0.3170 | +0.0215 (0.00) | 0.0030 / 0.0080 / 0.0002 | 0.00 |
| 250 | 0.2790 | 0.2837 | 0.2942 | 0.2818 | 0.2906 | 0.3000 | +0.0113 (0.04) | 0.0004 / 0.0048 / 0.0002 | 0.00 |
| 500 | 0.2787 | 0.2805 | 0.2894 | 0.2793 | 0.2848 | 0.2948 | +0.0063 (0.00) | 0.0002 / 0.0031 / 0.0001 | 0.00 |

## H_hypo_h199

603 patients, 9,321 landmarks, prevalence 0.216. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.4240 | 0.4282 | 0.4415 | 0.4260 | 0.4394 | 0.4554 | +0.0161 (0.04) | 0.0031 / 0.0111 / 0.0017 | 0.28 |
| 250 | 0.4218 | 0.4213 | 0.4280 | 0.4181 | 0.4244 | 0.4384 | +0.0069 (0.04) | 0.0030 / 0.0092 / 0.0026 | 0.04 |

## H_O2_h73

1,680 patients, 28,164 landmarks, prevalence 0.403. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': 500, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6276 | 0.6327 | 0.6628 | 0.6320 | 0.6604 | 0.6662 | +0.0319 (0.00) | 0.0089 / 0.0068 / 0.0033 | 0.00 |
| 250 | 0.6220 | 0.6216 | 0.6397 | 0.6192 | 0.6308 | 0.6415 | +0.0139 (0.00) | 0.0048 / 0.0105 / 0.0040 | 0.00 |
| 500 | 0.6220 | 0.6152 | 0.6251 | 0.6125 | 0.6206 | 0.6287 | +0.0082 (0.12) | 0.0028 / 0.0069 / 0.0073 | 0.00 |

## H_O2_h413

1,102 patients, 13,625 landmarks, prevalence 0.632. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6200 | 0.6168 | 0.6372 | 0.6153 | 0.6382 | 0.6437 | +0.0162 (0.16) | 0.0089 / 0.0288 / 0.0088 | 0.40 |
| 250 | 0.6157 | 0.6054 | 0.6094 | 0.5990 | 0.6031 | 0.6139 | -0.0010 (0.56) | 0.0079 / 0.0267 / 0.0131 | 0.24 |
| 500 | 0.6136 | 0.5920 | 0.5947 | 0.5867 | 0.5884 | 0.5939 | -0.0017 (0.60) | 0.0034 / 0.0235 / 0.0232 | 0.08 |

## H_O2_h167

941 patients, 12,157 landmarks, prevalence 0.527. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 500, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6261 | 0.6226 | 0.6508 | 0.6252 | 0.6494 | 0.6460 | +0.0196 (0.24) | 0.0087 / 0.0229 / 0.0089 | 0.40 |
| 250 | 0.6217 | 0.6085 | 0.6183 | 0.6033 | 0.6106 | 0.6180 | +0.0052 (0.32) | 0.0055 / 0.0253 / 0.0159 | 0.32 |
| 500 | 0.6197 | 0.5939 | 0.5974 | 0.5915 | 0.5921 | 0.6018 | -0.0000 (0.52) | 0.0054 / 0.0187 / 0.0289 | 0.32 |

## H_O2_h243

818 patients, 13,631 landmarks, prevalence 0.277. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 500, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5384 | 0.5353 | 0.5439 | 0.5278 | 0.5403 | 0.5370 | +0.0049 (0.44) | 0.0096 / 0.0302 / 0.0127 | 0.40 |
| 250 | 0.5370 | 0.5238 | 0.5268 | 0.5143 | 0.5171 | 0.5143 | -0.0031 (0.36) | 0.0106 / 0.0168 / 0.0192 | 0.20 |
| 500 | 0.5348 | 0.5062 | 0.5084 | 0.4989 | 0.5016 | 0.5047 | -0.0012 (0.48) | 0.0078 / 0.0190 / 0.0325 | 0.00 |

## H_O2_h420

772 patients, 12,277 landmarks, prevalence 0.315. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5509 | 0.5522 | 0.5908 | 0.5530 | 0.5912 | 0.5852 | +0.0333 (0.08) | 0.0085 / 0.0147 / 0.0060 | 0.16 |
| 250 | 0.5508 | 0.5398 | 0.5652 | 0.5349 | 0.5607 | 0.5573 | +0.0202 (0.12) | 0.0076 / 0.0147 / 0.0120 | 0.00 |
| 500 | 0.5476 | 0.5305 | 0.5487 | 0.5260 | 0.5433 | 0.5472 | +0.0153 (0.20) | 0.0045 / 0.0120 / 0.0189 | 0.00 |

## H_O2_h458

743 patients, 11,629 landmarks, prevalence 0.397. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 500, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5959 | 0.5905 | 0.6182 | 0.5935 | 0.6137 | 0.6322 | +0.0220 (0.16) | 0.0100 / 0.0006 / 0.0082 | 0.28 |
| 250 | 0.5920 | 0.5836 | 0.5916 | 0.5799 | 0.5828 | 0.5953 | +0.0014 (0.52) | 0.0058 / 0.0091 / 0.0126 | 0.04 |
| 500 | 0.5913 | 0.5734 | 0.5781 | 0.5698 | 0.5731 | 0.5845 | +0.0019 (0.56) | 0.0020 / 0.0108 / 0.0198 | 0.00 |

## H_O2_h338

729 patients, 10,864 landmarks, prevalence 0.422. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': 100, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5957 | 0.5855 | 0.6355 | 0.5874 | 0.6322 | 0.6335 | +0.0389 (0.00) | 0.0090 / 0.0092 / 0.0128 | 0.00 |
| 250 | 0.5882 | 0.5763 | 0.6044 | 0.5728 | 0.5982 | 0.6108 | +0.0204 (0.16) | 0.0019 / 0.0107 / 0.0126 | 0.00 |
| 500 | 0.5886 | 0.5702 | 0.5893 | 0.5687 | 0.5824 | 0.5968 | +0.0138 (0.20) | 0.0007 / 0.0106 / 0.0185 | 0.00 |

## H_O2_h252

711 patients, 11,559 landmarks, prevalence 0.391. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5979 | 0.5979 | 0.6395 | 0.6017 | 0.6395 | 0.6558 | +0.0379 (0.00) | 0.0045 / 0.0026 / 0.0042 | 0.16 |
| 250 | 0.5964 | 0.5934 | 0.6134 | 0.5941 | 0.6070 | 0.6220 | +0.0136 (0.16) | 0.0042 / 0.0030 / 0.0051 | 0.00 |
| 500 | 0.5946 | 0.5890 | 0.6033 | 0.5877 | 0.5994 | 0.6001 | +0.0079 (0.36) | 0.0048 / 0.0088 / 0.0095 | 0.00 |

## H_O2_h443

699 patients, 11,184 landmarks, prevalence 0.344. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5953 | 0.5993 | 0.6355 | 0.5999 | 0.6351 | 0.6499 | +0.0393 (0.00) | 0.0068 / 0.0056 / 0.0041 | 0.24 |
| 250 | 0.5928 | 0.5954 | 0.6148 | 0.5928 | 0.6076 | 0.6182 | +0.0151 (0.16) | 0.0041 / 0.0041 / 0.0021 | 0.16 |
| 500 | 0.5914 | 0.5922 | 0.6094 | 0.5889 | 0.6014 | 0.6109 | +0.0136 (0.16) | 0.0048 / 0.0073 / 0.0032 | 0.04 |

## H_O2_h300

663 patients, 9,323 landmarks, prevalence 0.452. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': 500, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6044 | 0.6143 | 0.6472 | 0.6111 | 0.6401 | 0.6364 | +0.0289 (0.04) | 0.0105 / 0.0066 / 0.0042 | 0.24 |
| 250 | 0.6028 | 0.5984 | 0.6206 | 0.5943 | 0.6087 | 0.6141 | +0.0133 (0.24) | 0.0054 / 0.0079 / 0.0078 | 0.08 |
| 500 | 0.6015 | 0.5870 | 0.6021 | 0.5836 | 0.5925 | 0.5983 | +0.0080 (0.32) | 0.0018 / 0.0140 / 0.0156 | 0.00 |

## H_O2_h152

661 patients, 8,125 landmarks, prevalence 0.594. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 100, 'update_vs_adopt': 100, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6307 | 0.6037 | 0.6099 | 0.5995 | 0.6086 | 0.6021 | +0.0003 (0.52) | 0.0121 / 0.0282 / 0.0328 | 0.72 |
| 250 | 0.6277 | 0.5795 | 0.5791 | 0.5700 | 0.5716 | 0.5779 | -0.0031 (0.60) | 0.0111 / 0.0457 / 0.0561 | 0.76 |
| 500 | 0.6262 | 0.5567 | 0.5649 | 0.5531 | 0.5567 | 0.5708 | +0.0034 (0.36) | 0.0027 / 0.0109 / 0.0706 | 0.96 |

## H_O2_h411

651 patients, 7,941 landmarks, prevalence 0.514. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 500, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6173 | 0.6066 | 0.6321 | 0.6085 | 0.6345 | 0.6399 | +0.0191 (0.20) | 0.0104 / 0.0173 / 0.0160 | 0.04 |
| 250 | 0.6088 | 0.5909 | 0.5983 | 0.5888 | 0.5937 | 0.5995 | +0.0023 (0.40) | 0.0086 / 0.0230 / 0.0216 | 0.00 |
| 500 | 0.6098 | 0.5761 | 0.5808 | 0.5764 | 0.5809 | 0.5846 | +0.0026 (0.44) | 0.0010 / 0.0186 / 0.0347 | 0.00 |

## H_O2_h264

650 patients, 10,001 landmarks, prevalence 0.355. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5935 | 0.6134 | 0.6293 | 0.6099 | 0.6266 | 0.6339 | +0.0265 (0.04) | 0.0095 / 0.0231 / 0.0002 | 0.00 |
| 250 | 0.5943 | 0.6045 | 0.6137 | 0.5980 | 0.6051 | 0.6174 | +0.0128 (0.08) | 0.0055 / 0.0236 / 0.0039 | 0.00 |
| 500 | 0.5928 | 0.5954 | 0.5974 | 0.5910 | 0.5938 | 0.5970 | +0.0042 (0.36) | 0.0053 / 0.0099 / 0.0044 | 0.00 |

## H_O2_h449

647 patients, 9,372 landmarks, prevalence 0.374. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 500, 'update_vs_adopt': 500, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6252 | 0.6283 | 0.6466 | 0.6331 | 0.6460 | 0.6406 | +0.0160 (0.16) | 0.0110 / 0.0140 / 0.0070 | 0.72 |
| 250 | 0.6194 | 0.6107 | 0.6132 | 0.6071 | 0.6089 | 0.6146 | -0.0009 (0.44) | 0.0081 / 0.0185 / 0.0144 | 0.88 |
| 500 | 0.6188 | 0.5975 | 0.6008 | 0.5968 | 0.6025 | 0.6065 | +0.0032 (0.32) | 0.0041 / 0.0133 / 0.0238 | 1.00 |

## H_O2_h199

603 patients, 9,321 landmarks, prevalence 0.238. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.5140 | 0.5217 | 0.5250 | 0.5165 | 0.5227 | 0.5238 | +0.0038 (0.44) | 0.0066 / 0.0278 / 0.0075 | 0.72 |
| 250 | 0.5110 | 0.5046 | 0.5072 | 0.4985 | 0.5024 | 0.4990 | +0.0024 (0.44) | 0.0169 / 0.0257 / 0.0175 | 0.76 |

## M_hypo_inspire_M0

11,631 patients, 148,293 landmarks, prevalence 0.132. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 4000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3250 | 0.3250 | 0.3355 | 0.3246 | 0.3316 | 0.3409 | +0.0077 (0.00) | 0.0010 / 0.0035 / 0.0008 | 0.30 |
| 1000 | 0.3239 | 0.3211 | 0.3233 | 0.3202 | 0.3217 | 0.3329 | +0.0015 (0.10) | 0.0011 / 0.0029 / 0.0029 | 0.00 |
| 4000 | 0.3237 | 0.3174 | 0.3180 | 0.3170 | 0.3178 | 0.3294 | +0.0006 (0.20) | 0.0003 / 0.0001 / 0.0001 | 0.00 |

## M_hypo_inspire_M1

11,631 patients, 148,293 landmarks, prevalence 0.132. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 1000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': 1000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3322 | 0.3332 | 0.3330 | 0.3292 | 0.3297 | 0.3395 | +0.0008 (0.40) | 0.0018 / 0.0017 / 0.0011 | 0.00 |
| 1000 | 0.3320 | 0.3247 | 0.3242 | 0.3229 | 0.3221 | 0.3333 | -0.0008 (0.90) | 0.0001 / 0.0030 / 0.0079 | 0.00 |
| 4000 | 0.3317 | 0.3189 | 0.3182 | 0.3188 | 0.3177 | 0.3294 | -0.0010 (0.90) | 0.0001 / 0.0003 / 0.0007 | 0.00 |

## M_hypo_inspire_M2

11,631 patients, 148,293 landmarks, prevalence 0.132. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 1000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3451 | 0.3363 | 0.3341 | 0.3322 | 0.3309 | 0.3410 | -0.0013 (0.70) | 0.0006 / 0.0067 / 0.0110 | 0.00 |
| 1000 | 0.3448 | 0.3260 | 0.3239 | 0.3245 | 0.3220 | 0.3328 | -0.0025 (1.00) | 0.0000 / 0.0018 / 0.0208 | 0.00 |
| 4000 | 0.3445 | 0.3201 | 0.3184 | 0.3197 | 0.3180 | 0.3296 | -0.0016 (1.00) | 0.0000 / 0.0010 / 0.0017 | 0.00 |

## M_hypo_inspire_M3

11,631 patients, 148,293 landmarks, prevalence 0.132. Break-even (≥ 80 %): {'build_vs_update': 1000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 1000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3428 | 0.3334 | 0.3329 | 0.3306 | 0.3299 | 0.3410 | -0.0005 (0.60) | 0.0035 / 0.0091 / 0.0106 | 0.00 |
| 1000 | 0.3427 | 0.3251 | 0.3239 | 0.3237 | 0.3222 | 0.3331 | -0.0015 (0.90) | 0.0001 / 0.0028 / 0.0188 | 0.00 |
| 4000 | 0.3425 | 0.3196 | 0.3180 | 0.3192 | 0.3177 | 0.3296 | -0.0016 (1.00) | 0.0000 / 0.0007 / 0.0016 | 0.00 |

## M_hypo_mimic_M0

24,464 patients, 387,158 landmarks, prevalence 0.307. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 4000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.4988 | 0.5026 | 0.5158 | 0.4997 | 0.5097 | 0.5169 | +0.0112 (0.00) | 0.0003 / 0.0080 / 0.0000 | 0.00 |
| 1000 | 0.4980 | 0.4968 | 0.5013 | 0.4953 | 0.4995 | 0.5067 | +0.0041 (0.00) | 0.0008 / 0.0012 / 0.0012 | 0.00 |
| 4000 | 0.4979 | 0.4927 | 0.4941 | 0.4925 | 0.4936 | 0.5019 | +0.0012 (0.00) | 0.0000 / 0.0005 / 0.0000 | 0.00 |

## M_hypo_mimic_M1

24,464 patients, 387,158 landmarks, prevalence 0.307. Break-even (≥ 80 %): {'build_vs_update': 1000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 4000, 'best_own_vs_best_ext': 4000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.5190 | 0.5142 | 0.5135 | 0.5082 | 0.5090 | 0.5160 | +0.0008 (0.20) | 0.0035 / 0.0103 / 0.0061 | 0.00 |
| 1000 | 0.5184 | 0.5020 | 0.5010 | 0.5001 | 0.4990 | 0.5059 | -0.0010 (0.70) | 0.0007 / 0.0009 / 0.0174 | 0.00 |
| 4000 | 0.5183 | 0.4960 | 0.4942 | 0.4957 | 0.4938 | 0.5020 | -0.0019 (1.00) | 0.0000 / 0.0009 / 0.0018 | 0.00 |

## M_hypo_mimic_M2

24,464 patients, 387,158 landmarks, prevalence 0.307. Break-even (≥ 80 %): {'build_vs_update': 1000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 1000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.5201 | 0.5115 | 0.5127 | 0.5071 | 0.5076 | 0.5156 | +0.0004 (0.60) | 0.0015 / 0.0074 / 0.0089 | 0.00 |
| 1000 | 0.5198 | 0.5021 | 0.5009 | 0.5004 | 0.4989 | 0.5050 | -0.0015 (1.00) | 0.0000 / 0.0012 / 0.0189 | 0.00 |
| 4000 | 0.5197 | 0.4959 | 0.4942 | 0.4957 | 0.4938 | 0.5019 | -0.0019 (1.00) | 0.0000 / 0.0009 / 0.0018 | 0.00 |

## M_hypo_mimic_M3

24,464 patients, 387,158 landmarks, prevalence 0.307. Break-even (≥ 80 %): {'build_vs_update': 1000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 1000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.5194 | 0.5125 | 0.5134 | 0.5086 | 0.5085 | 0.5157 | -0.0001 (0.40) | 0.0025 / 0.0065 / 0.0075 | 0.00 |
| 1000 | 0.5193 | 0.5021 | 0.5011 | 0.5005 | 0.4988 | 0.5054 | -0.0017 (1.00) | 0.0004 / 0.0026 / 0.0183 | 0.00 |
| 4000 | 0.5191 | 0.4960 | 0.4942 | 0.4958 | 0.4936 | 0.5020 | -0.0022 (1.00) | 0.0000 / 0.0011 / 0.0018 | 0.00 |

## M_hypo_eicu_M0

32,032 patients, 466,384 landmarks, prevalence 0.193. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': 4000, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3890 | 0.3928 | 0.4058 | 0.3903 | 0.3998 | 0.4086 | +0.0110 (0.00) | 0.0000 / 0.0067 / 0.0000 | 0.10 |
| 1000 | 0.3885 | 0.3894 | 0.3947 | 0.3880 | 0.3919 | 0.4003 | +0.0039 (0.00) | 0.0001 / 0.0011 / 0.0001 | 0.00 |
| 4000 | 0.3884 | 0.3865 | 0.3884 | 0.3862 | 0.3879 | 0.3968 | +0.0017 (0.00) | 0.0000 / 0.0014 / 0.0000 | 0.00 |

## M_hypo_eicu_M1

32,032 patients, 466,384 landmarks, prevalence 0.193. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 1000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.3984 | 0.4043 | 0.4067 | 0.3983 | 0.4017 | 0.4118 | +0.0039 (0.00) | 0.0023 / -0.0002 / 0.0000 | 0.00 |
| 1000 | 0.3976 | 0.3930 | 0.3947 | 0.3908 | 0.3923 | 0.3998 | +0.0015 (0.00) | 0.0017 / 0.0034 / 0.0046 | 0.00 |
| 4000 | 0.3975 | 0.3886 | 0.3884 | 0.3881 | 0.3879 | 0.3968 | -0.0002 (0.70) | 0.0001 / 0.0002 / 0.0002 | 0.00 |

## M_hypo_eicu_M2

32,032 patients, 466,384 landmarks, prevalence 0.193. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 1000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': 1000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.4046 | 0.4051 | 0.4058 | 0.3998 | 0.4014 | 0.4106 | +0.0016 (0.30) | 0.0019 / 0.0009 / 0.0012 | 0.10 |
| 1000 | 0.4039 | 0.3952 | 0.3945 | 0.3934 | 0.3923 | 0.4004 | -0.0011 (0.90) | 0.0009 / 0.0059 / 0.0096 | 0.00 |
| 4000 | 0.4038 | 0.3895 | 0.3884 | 0.3890 | 0.3877 | 0.3968 | -0.0012 (1.00) | 0.0000 / 0.0008 / 0.0010 | 0.00 |

## M_hypo_eicu_M3

32,032 patients, 466,384 landmarks, prevalence 0.193. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 1000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': 4000, 'best_own_vs_best_ext': 4000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.4046 | 0.4053 | 0.4072 | 0.4009 | 0.4029 | 0.4105 | +0.0022 (0.20) | 0.0024 / 0.0011 / 0.0014 | 0.00 |
| 1000 | 0.4032 | 0.3941 | 0.3943 | 0.3924 | 0.3918 | 0.4005 | -0.0005 (0.70) | 0.0002 / 0.0068 / 0.0094 | 0.00 |
| 4000 | 0.4030 | 0.3891 | 0.3883 | 0.3888 | 0.3878 | 0.3969 | -0.0010 (1.00) | 0.0002 / 0.0008 / 0.0008 | 0.00 |

## M_O1_mimic_M0

23,056 patients, 305,427 landmarks, prevalence 0.022. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 1000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': 4000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0946 | 0.0958 | 0.0983 | 0.0957 | 0.0969 | 0.0955 | +0.0006 (0.30) | 0.0009 / 0.0065 / 0.0001 | 1.00 |
| 1000 | 0.0942 | 0.0921 | 0.0929 | 0.0911 | 0.0914 | 0.0906 | -0.0005 (0.80) | 0.0002 / 0.0031 / 0.0009 | 1.00 |
| 4000 | 0.0940 | 0.0890 | 0.0890 | 0.0888 | 0.0881 | 0.0887 | -0.0006 (0.80) | 0.0003 / 0.0002 / 0.0002 | 1.00 |

## M_O1_mimic_M1

23,056 patients, 305,427 landmarks, prevalence 0.022. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0997 | 0.0972 | 0.0974 | 0.0971 | 0.0971 | 0.0949 | -0.0023 (0.90) | 0.0013 / 0.0083 / 0.0032 | 1.00 |
| 1000 | 0.0991 | 0.0938 | 0.0934 | 0.0928 | 0.0915 | 0.0906 | -0.0022 (1.00) | 0.0004 / 0.0016 / 0.0003 | 1.00 |
| 4000 | 0.0990 | 0.0897 | 0.0891 | 0.0895 | 0.0882 | 0.0887 | -0.0013 (1.00) | 0.0002 / 0.0006 / 0.0000 | 1.00 |

## M_O1_mimic_M2

23,056 patients, 305,427 landmarks, prevalence 0.022. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 4000, 'best_own_vs_best_ext': 1000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0999 | 0.0964 | 0.0979 | 0.0962 | 0.0972 | 0.0959 | -0.0004 (0.60) | 0.0007 / 0.0082 / 0.0036 | 1.00 |
| 1000 | 0.0993 | 0.0926 | 0.0932 | 0.0918 | 0.0914 | 0.0908 | -0.0010 (0.90) | 0.0005 / 0.0026 / 0.0006 | 1.00 |
| 4000 | 0.0991 | 0.0893 | 0.0891 | 0.0889 | 0.0882 | 0.0888 | -0.0007 (1.00) | 0.0003 / 0.0003 / 0.0001 | 1.00 |

## M_O1_mimic_M3

23,056 patients, 305,427 landmarks, prevalence 0.022. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 1000, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0995 | 0.0974 | 0.0971 | 0.0979 | 0.0972 | 0.0952 | -0.0025 (1.00) | 0.0020 / 0.0066 / 0.0030 | 1.00 |
| 1000 | 0.0988 | 0.0931 | 0.0934 | 0.0924 | 0.0913 | 0.0906 | -0.0020 (1.00) | 0.0004 / 0.0021 / 0.0005 | 1.00 |
| 4000 | 0.0986 | 0.0893 | 0.0888 | 0.0891 | 0.0881 | 0.0887 | -0.0010 (1.00) | 0.0002 / 0.0004 / 0.0000 | 1.00 |

## M_O1_eicu_M0

31,605 patients, 433,173 landmarks, prevalence 0.026. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 1000, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 4000, 'best_own_vs_best_ext': 4000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0954 | 0.0921 | 0.0938 | 0.0914 | 0.0916 | 0.0948 | +0.0006 (0.40) | 0.0024 / 0.0073 / 0.0038 | 0.00 |
| 1000 | 0.0951 | 0.0879 | 0.0891 | 0.0865 | 0.0864 | 0.0893 | -0.0001 (0.50) | 0.0003 / 0.0055 / 0.0073 | 0.00 |
| 4000 | 0.0947 | 0.0836 | 0.0833 | 0.0831 | 0.0827 | 0.0867 | -0.0004 (0.80) | 0.0003 / 0.0004 / 0.0004 | 0.00 |

## M_O1_eicu_M1

31,605 patients, 433,173 landmarks, prevalence 0.026. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.1048 | 0.0966 | 0.0948 | 0.0967 | 0.0931 | 0.0962 | -0.0034 (1.00) | 0.0014 / 0.0184 / 0.0101 | 0.60 |
| 1000 | 0.1039 | 0.0897 | 0.0889 | 0.0889 | 0.0867 | 0.0888 | -0.0021 (0.90) | 0.0004 / 0.0023 / 0.0034 | 0.80 |
| 4000 | 0.1035 | 0.0851 | 0.0833 | 0.0852 | 0.0827 | 0.0869 | -0.0023 (1.00) | 0.0000 / 0.0011 / 0.0004 | 0.80 |

## M_O1_eicu_M2

31,605 patients, 433,173 landmarks, prevalence 0.026. Break-even (≥ 80 %): {'build_vs_update': 1000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.1130 | 0.0975 | 0.0970 | 0.0971 | 0.0952 | 0.0949 | -0.0029 (0.90) | 0.0007 / 0.0111 / 0.0166 | 0.90 |
| 1000 | 0.1121 | 0.0898 | 0.0894 | 0.0886 | 0.0867 | 0.0893 | -0.0020 (0.90) | 0.0003 / 0.0029 / 0.0002 | 1.00 |
| 4000 | 0.1119 | 0.0845 | 0.0835 | 0.0843 | 0.0826 | 0.0867 | -0.0016 (1.00) | 0.0001 / 0.0008 / 0.0000 | 1.00 |

## M_O1_eicu_M3

31,605 patients, 433,173 landmarks, prevalence 0.026. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.1160 | 0.0984 | 0.0971 | 0.0977 | 0.0952 | 0.0971 | -0.0028 (0.80) | 0.0029 / 0.0141 / 0.0197 | 0.90 |
| 1000 | 0.1138 | 0.0899 | 0.0896 | 0.0886 | 0.0866 | 0.0897 | -0.0020 (0.90) | 0.0002 / 0.0002 / 0.0001 | 1.00 |
| 4000 | 0.1136 | 0.0845 | 0.0836 | 0.0842 | 0.0827 | 0.0866 | -0.0015 (1.00) | 0.0002 / 0.0006 / 0.0000 | 1.00 |

## M_O2_inspire_M0

11,631 patients, 148,293 landmarks, prevalence 0.587. Break-even (≥ 80 %): {'build_vs_update': 4000, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 4000, 'best_own_vs_best_ext': 4000}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6599 | 0.5802 | 0.5842 | 0.5667 | 0.5776 | 0.5742 | +0.0035 (0.30) | 0.0024 / 0.0197 / 0.0823 | 0.80 |
| 1000 | 0.6581 | 0.5417 | 0.5416 | 0.5384 | 0.5395 | 0.5513 | +0.0013 (0.40) | 0.0019 / 0.0023 / 0.0479 | 0.60 |
| 4000 | 0.6570 | 0.5194 | 0.5174 | 0.5197 | 0.5179 | 0.5455 | -0.0019 (0.80) | 0.0001 / 0.0021 / 0.0001 | 1.00 |

## M_O2_inspire_M1

11,631 patients, 148,293 landmarks, prevalence 0.587. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6745 | 0.6004 | 0.5852 | 0.5919 | 0.5769 | 0.5769 | -0.0187 (1.00) | 0.0007 / 0.0588 / 0.0893 | 1.00 |
| 1000 | 0.6706 | 0.5475 | 0.5400 | 0.5461 | 0.5384 | 0.5524 | -0.0073 (1.00) | 0.0000 / 0.0052 / 0.0000 | 1.00 |
| 4000 | 0.6696 | 0.5231 | 0.5186 | 0.5235 | 0.5188 | 0.5454 | -0.0048 (1.00) | 0.0000 / 0.0028 / 0.0000 | 1.00 |

## M_O2_inspire_M2

11,631 patients, 148,293 landmarks, prevalence 0.587. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6746 | 0.6017 | 0.5879 | 0.5937 | 0.5790 | 0.5732 | -0.0214 (1.00) | 0.0000 / 0.0505 / 0.0868 | 1.00 |
| 1000 | 0.6711 | 0.5537 | 0.5434 | 0.5507 | 0.5404 | 0.5522 | -0.0102 (1.00) | 0.0000 / 0.0046 / 0.0000 | 1.00 |
| 4000 | 0.6709 | 0.5233 | 0.5185 | 0.5239 | 0.5188 | 0.5458 | -0.0047 (0.90) | 0.0001 / 0.0019 / 0.0001 | 1.00 |

## M_O2_inspire_M3

11,631 patients, 148,293 landmarks, prevalence 0.587. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6686 | 0.6115 | 0.5967 | 0.6057 | 0.5877 | 0.5830 | -0.0244 (1.00) | 0.0021 / 0.0290 / 0.0719 | 1.00 |
| 1000 | 0.6627 | 0.5529 | 0.5439 | 0.5501 | 0.5402 | 0.5527 | -0.0099 (1.00) | 0.0000 / 0.0045 / 0.0000 | 1.00 |
| 4000 | 0.6624 | 0.5235 | 0.5181 | 0.5242 | 0.5187 | 0.5451 | -0.0053 (1.00) | 0.0000 / 0.0007 / 0.0000 | 1.00 |

## M_O2_mimic_M0

24,464 patients, 387,158 landmarks, prevalence 0.365. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 4000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.5648 | 0.5668 | 0.5910 | 0.5648 | 0.5829 | 0.5921 | +0.0178 (0.00) | 0.0015 / 0.0055 / 0.0006 | 0.20 |
| 1000 | 0.5627 | 0.5539 | 0.5613 | 0.5515 | 0.5583 | 0.5685 | +0.0068 (0.00) | 0.0003 / 0.0122 / 0.0088 | 0.00 |
| 4000 | 0.5624 | 0.5419 | 0.5427 | 0.5419 | 0.5431 | 0.5636 | +0.0009 (0.40) | 0.0009 / 0.0005 / 0.0005 | 0.00 |

## M_O2_mimic_M1

24,464 patients, 387,158 landmarks, prevalence 0.365. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6455 | 0.6026 | 0.5884 | 0.5929 | 0.5811 | 0.5873 | -0.0119 (1.00) | 0.0030 / 0.0222 / 0.0572 | 0.90 |
| 1000 | 0.6421 | 0.5660 | 0.5595 | 0.5634 | 0.5571 | 0.5687 | -0.0063 (1.00) | 0.0000 / 0.0036 / 0.0000 | 1.00 |
| 4000 | 0.6419 | 0.5467 | 0.5418 | 0.5470 | 0.5421 | 0.5632 | -0.0048 (1.00) | 0.0000 / 0.0010 / 0.0000 | 1.00 |

## M_O2_mimic_M2

24,464 patients, 387,158 landmarks, prevalence 0.365. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6571 | 0.6170 | 0.5906 | 0.6077 | 0.5833 | 0.5919 | -0.0247 (1.00) | 0.0000 / 0.0446 / 0.0665 | 1.00 |
| 1000 | 0.6564 | 0.5714 | 0.5594 | 0.5680 | 0.5576 | 0.5689 | -0.0106 (1.00) | 0.0000 / 0.0105 / 0.0000 | 1.00 |
| 4000 | 0.6557 | 0.5486 | 0.5426 | 0.5484 | 0.5430 | 0.5633 | -0.0057 (1.00) | 0.0000 / 0.0011 / 0.0000 | 1.00 |

## M_O2_mimic_M3

24,464 patients, 387,158 landmarks, prevalence 0.365. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6585 | 0.6088 | 0.5881 | 0.6000 | 0.5795 | 0.5902 | -0.0205 (1.00) | 0.0000 / 0.0182 / 0.0704 | 1.00 |
| 1000 | 0.6566 | 0.5704 | 0.5598 | 0.5667 | 0.5574 | 0.5698 | -0.0093 (1.00) | 0.0000 / 0.0050 / 0.0000 | 1.00 |
| 4000 | 0.6562 | 0.5476 | 0.5422 | 0.5477 | 0.5422 | 0.5632 | -0.0050 (1.00) | 0.0000 / 0.0006 / 0.0000 | 1.00 |

## M_O2_eicu_M0

32,032 patients, 466,384 landmarks, prevalence 0.418. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 1000, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6275 | 0.6267 | 0.6471 | 0.6244 | 0.6416 | 0.6550 | +0.0178 (0.00) | 0.0017 / 0.0027 / 0.0023 | 0.50 |
| 1000 | 0.6261 | 0.6152 | 0.6238 | 0.6144 | 0.6201 | 0.6239 | +0.0060 (0.00) | 0.0014 / 0.0054 / 0.0109 | 0.10 |
| 4000 | 0.6252 | 0.6065 | 0.6078 | 0.6060 | 0.6077 | 0.6172 | +0.0015 (0.00) | 0.0000 / 0.0000 / 0.0000 | 0.00 |

## M_O2_eicu_M1

32,032 patients, 466,384 landmarks, prevalence 0.418. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6540 | 0.6554 | 0.6464 | 0.6426 | 0.6383 | 0.6482 | -0.0046 (0.80) | 0.0070 / 0.0140 / 0.0089 | 0.90 |
| 1000 | 0.6526 | 0.6270 | 0.6221 | 0.6236 | 0.6190 | 0.6237 | -0.0047 (1.00) | 0.0011 / 0.0121 / 0.0000 | 1.00 |
| 4000 | 0.6522 | 0.6114 | 0.6069 | 0.6105 | 0.6064 | 0.6169 | -0.0042 (1.00) | 0.0000 / 0.0031 / 0.0000 | 1.00 |

## M_O2_eicu_M2

32,032 patients, 466,384 landmarks, prevalence 0.418. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6823 | 0.6782 | 0.6476 | 0.6559 | 0.6422 | 0.6505 | -0.0148 (1.00) | 0.0000 / 0.0258 / 0.0347 | 1.00 |
| 1000 | 0.6802 | 0.6343 | 0.6235 | 0.6272 | 0.6205 | 0.6245 | -0.0067 (1.00) | 0.0000 / 0.0038 / 0.0000 | 1.00 |
| 4000 | 0.6796 | 0.6126 | 0.6077 | 0.6114 | 0.6070 | 0.6168 | -0.0045 (1.00) | 0.0000 / 0.0018 / 0.0000 | 1.00 |

## M_O2_eicu_M3

32,032 patients, 466,384 landmarks, prevalence 0.418. Break-even (≥ 80 %): {'build_vs_update': 250, 'build_vs_adopt': 250, 'update_vs_adopt': 1000, 'build_tuned_vs_update_tuned': 250, 'best_own_vs_best_ext': 250}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.6816 | 0.6781 | 0.6468 | 0.6530 | 0.6378 | 0.6453 | -0.0157 (1.00) | 0.0012 / 0.0357 / 0.0348 | 1.00 |
| 1000 | 0.6801 | 0.6337 | 0.6232 | 0.6260 | 0.6201 | 0.6254 | -0.0060 (1.00) | 0.0000 / 0.0063 / 0.0000 | 1.00 |
| 4000 | 0.6798 | 0.6110 | 0.6075 | 0.6098 | 0.6067 | 0.6169 | -0.0033 (1.00) | 0.0000 / 0.0013 / 0.0000 | 1.00 |

## T_hypo_mimic

24,464 patients, 387,158 landmarks, prevalence 0.307. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 4000, 'update_vs_adopt': 500, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.4823 | 0.4820 | 0.5020 | 0.4813 | 0.4969 | 0.5042 | +0.0160 (0.00) | 0.0007 / 0.0025 / 0.0007 | 0.20 |
| 500 | 0.4827 | 0.4804 | 0.4926 | 0.4808 | 0.4889 | 0.4969 | +0.0090 (0.00) | 0.0023 / 0.0020 / 0.0024 | 0.00 |
| 1000 | 0.4824 | 0.4800 | 0.4881 | 0.4802 | 0.4864 | 0.4947 | +0.0065 (0.00) | 0.0012 / 0.0021 / 0.0024 | 0.00 |
| 2000 | 0.4822 | 0.4789 | 0.4836 | 0.4797 | 0.4826 | 0.4905 | +0.0037 (0.00) | 0.0000 / 0.0020 / 0.0033 | 0.00 |
| 4000 | 0.4829 | 0.4795 | 0.4820 | 0.4799 | 0.4818 | 0.4913 | +0.0022 (0.00) | 0.0000 / 0.0000 / 0.0000 | 0.00 |

## T_O1_mimic

23,056 patients, 305,427 landmarks, prevalence 0.022. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': None, 'update_vs_adopt': None, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.0669 | 0.0691 | 0.0706 | 0.0689 | 0.0709 | 0.0706 | +0.0028 (0.00) | 0.0014 / 0.0041 / 0.0000 | 0.90 |
| 500 | 0.0670 | 0.0676 | 0.0700 | 0.0672 | 0.0694 | 0.0687 | +0.0019 (0.00) | 0.0012 / 0.0009 / 0.0002 | 1.00 |
| 1000 | 0.0669 | 0.0682 | 0.0701 | 0.0676 | 0.0697 | 0.0684 | +0.0015 (0.00) | 0.0016 / 0.0006 / 0.0032 | 1.00 |
| 2000 | 0.0666 | 0.0680 | 0.0684 | 0.0670 | 0.0679 | 0.0670 | +0.0005 (0.20) | 0.0014 / 0.0011 / 0.0018 | 1.00 |
| 4000 | 0.0669 | 0.0674 | 0.0675 | 0.0671 | 0.0673 | 0.0671 | +0.0002 (0.40) | 0.0007 / 0.0006 / 0.0007 | 1.00 |

## T_O2_mimic

24,464 patients, 387,158 landmarks, prevalence 0.365. Break-even (≥ 80 %): {'build_vs_update': None, 'build_vs_adopt': 2000, 'update_vs_adopt': 250, 'build_tuned_vs_update_tuned': None, 'best_own_vs_best_ext': None}.

| n | adopt | update | build | update_tuned | build_tuned | build_lr | best own − best ext (wins) | regret cv / closed / v2 | flagged |
|---|---|---|---|---|---|---|---|---|---|
| 250 | 0.5875 | 0.5827 | 0.6079 | 0.5833 | 0.6000 | 0.6171 | +0.0193 (0.00) | 0.0043 / 0.0089 / 0.0057 | 0.00 |
| 500 | 0.5848 | 0.5789 | 0.5908 | 0.5762 | 0.5866 | 0.5974 | +0.0103 (0.00) | 0.0039 / 0.0101 / 0.0059 | 0.00 |
| 1000 | 0.5856 | 0.5751 | 0.5863 | 0.5746 | 0.5846 | 0.5957 | +0.0103 (0.00) | 0.0007 / 0.0102 / 0.0105 | 0.00 |
| 2000 | 0.5850 | 0.5685 | 0.5752 | 0.5681 | 0.5769 | 0.5906 | +0.0070 (0.00) | 0.0012 / 0.0081 / 0.0165 | 0.00 |
| 4000 | 0.5854 | 0.5646 | 0.5695 | 0.5646 | 0.5702 | 0.5894 | +0.0053 (0.00) | 0.0000 / 0.0000 / 0.0000 | 0.00 |

