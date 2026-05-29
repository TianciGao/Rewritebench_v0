# Pre/Post Fix Comparison

Pre-fix input route card: `audits/calcite_hep_pg_local_metrics_projection_v0/`.

| field | before | after | delta |
| --- | ---: | ---: | ---: |
| generated_candidate_rows | 33 | 33 | 0 |
| candidate_executable_rows | 23 | 28 | +5 |
| exact_rows | 20 | 22 | +2 |
| mismatch_rows | 3 | 6 | +3 |
| candidate_execution_failed_rows | 8 | 0 | -8 |
| no_candidate_rows | 7 | 7 | 0 |
| timed_exact_rows | 20 | 22 | +2 |
| diagnostic_gm_speedup | 0.995749 | 1.009852 | +0.014103 |

Interpretation:

- Identifier quoting fix improved candidate execution coverage from 23/40 to 28/40.
- Exact/result-consistent rows increased from 20 to 22.
- `CONS_0037` became exact after quote normalization.
- `CONS_0011` also became exact under the broader DDL-backed identifier normalization.
- Mismatches increased because previously failing generated candidates now execute and reach the checker.
- Candidate execution failures dropped to zero under the policy used here because schema-fallback candidates are excluded rather than executed.

This remains a local diagnostic route-card comparison only.
