# Engine Metrics Review

Source of truth:

```text
runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_by_engine.csv
```

Canonical per-engine rows copied from `local_metrics_by_engine.csv`:

| Engine | Selected | Generated | Source executable | Candidate executable | Exact | Mismatch | Label-only mismatch | Unsupported fail-closed | Timed | GM speedup | P10 | P25 | P50 | P75 | P90 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mysql | 40 | 33 | 33 | 33 | 26 | 7 | 3 | 0 | 26 | 0.9975822183870096 | 0.9758378282188593 | 0.9901402785301716 | 0.9987851018424811 | 1.0064745974586937 | 1.0125418939496604 |
| postgres | 40 | 33 | 33 | 32 | 25 | 7 | 1 | 0 | 24 | 0.9864197011359102 | 0.9833233350057817 | 0.9900795112842352 | 0.9956643747567999 | 1.0014944335015785 | 1.0181705381131736 |
| spark | 40 | 33 | 32 | 30 | 30 | 0 | 0 | 1 | 30 | 0.9736707438200914 | 0.8697380672195196 | 0.9374356800342252 | 0.9833197823642154 | 1.0164132754934743 | 1.087712096098167 |

Canonical per-engine rates:

| Engine | Generation rate | Execution coverage rate | Result consistency rate |
| --- | ---: | ---: | ---: |
| mysql | 0.825 | 0.825 | 0.65 |
| postgres | 0.825 | 0.8 | 0.625 |
| spark | 0.825 | 0.75 | 0.75 |

The performance denominator is each engine's own strict exact timed row set.
