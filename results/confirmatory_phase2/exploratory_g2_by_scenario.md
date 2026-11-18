# Phase 2, exploratory: accuracy of the per-sample shift diagnosis by scenario

Declared exploratory (pre-registration section 7 spirit; not a registered analysis). Same estimator as G2
(risk difference of "best own beats best external" between flagged and unflagged samples, bootstrap clustered
by unit, 95 % CI), computed within each scenario. Source: `exploratory_g2_by_scenario.json`.

| scenario | units | samples | flagged | own wins | risk difference (95 % CI) | sensitivity | PPV | NPV |
|---|---|---|---|---|---|---|---|---|
| H, single eICU hospitals | 30 | 2,200 | 385 | 335 | 0.074 (−0.059 to 0.177) | 0.25 | 0.21 | 0.86 |
| T, MIMIC-IV over time | 3 | 120 | 41 | 3 | 0.073 (0.000 to 0.077) | 1.00 | 0.07 | 1.00 |
| M0, no harmonization error | 8 | 240 | 66 | 58 | 0.315 (−0.192 to 0.498) | 0.53 | 0.47 | 0.85 |
| M1–M3, harmonization errors | 24 | 720 | 439 | 626 | 0.241 (0.132 to 0.379) | 0.68 | 0.96 | 0.28 |
| H + T + M0 (no induced error) | 41 | 2,560 | 492 | 396 | 0.100 (−0.010 to 0.200) | 0.29 | 0.24 | 0.87 |

Reading (descriptive): the pooled G2 signal comes mainly from the harmonization-error scenario. Without induced
errors the interval includes 0, and in single hospitals a flagged sample is followed by an own-model win in about
one case in five.
