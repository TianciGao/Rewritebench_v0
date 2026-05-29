# Engine Metrics Review

Source: `runs/user/sqlglot_noop_track_a_120_canonical_v0/metrics/local_metrics_by_engine.csv`

Canonical per-engine rows copied from `local_metrics_by_engine.csv`:

| Engine | Selected | Generated | Source executable | Candidate executable | Exact | Mismatch | Label-only mismatch | Unsupported fail-closed | Timed | GM speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PostgreSQL | 40 | 35 | 35 | 35 | 35 | 0 | 0 | 0 | 35 | 0.965868094391865 |
| MySQL | 40 | 40 | 40 | 39 | 31 | 8 | 5 | 0 | 31 | 0.9987204731888261 |
| Spark | 40 | 40 | 35 | 33 | 31 | 2 | 0 | 5 | 31 | 0.9770158651493955 |

Canonical speedup percentiles:

| Engine | P10 | P25 | P50 | P75 | P90 |
| --- | ---: | ---: | ---: | ---: | ---: |
| PostgreSQL | 0.9605204331893996 | 0.9859658779489223 | 0.9972168165995098 | 1.004002204296833 | 1.0145143573114221 |
| MySQL | 0.9791479810863389 | 0.986542542953672 | 0.9990347055565928 | 1.0101401774509113 | 1.017464028723815 |
| Spark | 0.8868759874397418 | 0.9522486641008008 | 0.9952991764068027 | 1.026703840937277 | 1.0440854774625992 |

These are local diagnostic values over each engine's strict exact-timed rows only.
