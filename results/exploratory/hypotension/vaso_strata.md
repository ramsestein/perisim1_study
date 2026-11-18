# Vasopressor stratum in every unit (post hoc, exploratory; internal review 8, R8)

Transported LightGBM after logistic recalibration on all local labels. CITL and slope within the stratum; Δ log-loss recalibrated − own and recalibrated − update (nats; 95 % patient-bootstrap CI).

| unit | stratum | patients | prevalence | CITL | slope | recal − own | recal − update |
|---|---|---|---|---|---|---|---|
| hypo_inspire | vaso_on=0 | — | — | fewer than 100 patients or 10 events | | | |
| hypo_inspire | vaso_on=1 | — | — | fewer than 100 patients or 10 events | | | |
| hypo_inspire | replicates (rule fixed in DECISIONS) | None | | | | | |
| hypo_mimic | vaso_on=0 | 23,056 | 0.267 | -0.080 (-0.094 to -0.064) | +1.004 (+0.991 to +1.017) | +0.0053 (+0.0047 to +0.0060) | +0.0055 (+0.0050 to +0.0060) |
| hypo_mimic | vaso_on=1 | 10,941 | 0.456 | +0.233 (+0.205 to +0.258) | +0.878 (+0.855 to +0.901) | +0.0143 (+0.0125 to +0.0162) | +0.0145 (+0.0128 to +0.0161) |
| hypo_mimic | replicates (rule fixed in DECISIONS) | True | | | | | |
| hypo_eicu | vaso_on=0 | 31,605 | 0.185 | +0.037 (+0.022 to +0.052) | +1.018 (+1.006 to +1.029) | +0.0022 (+0.0018 to +0.0027) | +0.0027 (+0.0024 to +0.0030) |
| hypo_eicu | vaso_on=1 | 5,325 | 0.306 | -0.311 (-0.351 to -0.269) | +1.088 (+1.042 to +1.129) | +0.0128 (+0.0100 to +0.0155) | +0.0134 (+0.0110 to +0.0156) |
| hypo_eicu | replicates (rule fixed in DECISIONS) | True | | | | | |
| nwicu_inspire | vaso_on=0 | 1,989 | 0.111 | +0.049 (-0.025 to +0.115) | +1.035 (+0.980 to +1.091) | -0.0043 (-0.0064 to -0.0021) | -0.0018 (-0.0037 to +0.0000) |
| nwicu_inspire | vaso_on=1 | 648 | 0.247 | -0.159 (-0.293 to -0.033) | +0.960 (+0.816 to +1.105) | -0.0045 (-0.0149 to +0.0042) | -0.0078 (-0.0135 to -0.0019) |
| nwicu_inspire | replicates (rule fixed in DECISIONS) | False | | | | | |
| nwicu_mimic | vaso_on=0 | 1,989 | 0.111 | -0.017 (-0.090 to +0.052) | +1.011 (+0.961 to +1.064) | -0.0040 (-0.0062 to -0.0020) | -0.0011 (-0.0028 to +0.0006) |
| nwicu_mimic | vaso_on=1 | 648 | 0.247 | +0.060 (-0.070 to +0.188) | +0.869 (+0.739 to +1.005) | -0.0054 (-0.0132 to +0.0023) | -0.0033 (-0.0089 to +0.0029) |
| nwicu_mimic | replicates (rule fixed in DECISIONS) | False | | | | | |
| nwicu_eicu | vaso_on=0 | 1,989 | 0.111 | +0.065 (-0.009 to +0.133) | +1.051 (+0.994 to +1.110) | -0.0036 (-0.0057 to -0.0013) | -0.0009 (-0.0029 to +0.0011) |
| nwicu_eicu | vaso_on=1 | 648 | 0.247 | -0.208 (-0.341 to -0.078) | +0.955 (+0.806 to +1.103) | -0.0000 (-0.0106 to +0.0099) | -0.0053 (-0.0123 to +0.0014) |
| nwicu_eicu | replicates (rule fixed in DECISIONS) | False | | | | | |
