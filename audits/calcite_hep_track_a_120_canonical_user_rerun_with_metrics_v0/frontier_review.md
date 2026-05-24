# Frontier Review

Source of truth:

```text
runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_summary.json
runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_timing_speedup_rows.csv
```

Canonical `diagnostic_status_counts`:

```text
exact_status:
  exact: 81
  mismatch: 14
  not_evaluated_non_db_mvp: 21
  not_exact_due_to_execution_failure: 4

failure_bucket:
  none: 81
  mismatch: 14
  no_candidate_sql: 21
  candidate_execution_failed: 3
  unsupported_engine: 1

timing_status:
  timed: 80
  not_eligible: 40
```

Non-exact rows copied from canonical `local_timing_speedup_rows.csv`:

| Engine | Case | Pool | Exact status | Failure bucket | Label-only mismatch | Timing status |
| --- | --- | --- | --- | --- | --- | --- |
| mysql | CONS_0037 | CONS | mismatch | mismatch | true | not_eligible |
| mysql | LONGTAIL_0012 | LONGTAIL | mismatch | mismatch | false | not_eligible |
| mysql | LONGTAIL_0013 | LONGTAIL | mismatch | mismatch | false | not_eligible |
| mysql | PERF_0035 | PERF | mismatch | mismatch | false | not_eligible |
| mysql | PERF_0062 | PERF | mismatch | mismatch | false | not_eligible |
| mysql | PORT_0003 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| mysql | PORT_0004 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| mysql | PORT_0005 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| mysql | PORT_0008 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| mysql | PORT_0012 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| mysql | PORT_0013 | PORT | mismatch | mismatch | true | not_eligible |
| mysql | PORT_0022 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| mysql | PORT_0024 | PORT | mismatch | mismatch | true | not_eligible |
| mysql | PORT_0025 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| postgres | CONS_0036 | CONS | mismatch | mismatch | true | not_eligible |
| postgres | LONGTAIL_0011 | LONGTAIL | mismatch | mismatch | false | not_eligible |
| postgres | LONGTAIL_0012 | LONGTAIL | mismatch | mismatch | false | not_eligible |
| postgres | LONGTAIL_0013 | LONGTAIL | mismatch | mismatch | false | not_eligible |
| postgres | LONGTAIL_0022 | LONGTAIL | mismatch | mismatch | false | not_eligible |
| postgres | PERF_0035 | PERF | mismatch | mismatch | false | not_eligible |
| postgres | PERF_0062 | PERF | mismatch | mismatch | false | not_eligible |
| postgres | PORT_0003 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| postgres | PORT_0004 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| postgres | PORT_0005 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| postgres | PORT_0008 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| postgres | PORT_0012 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| postgres | PORT_0013 | PORT | not_exact_due_to_execution_failure | candidate_execution_failed | false | not_eligible |
| postgres | PORT_0022 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| postgres | PORT_0025 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| spark | PERF_0062 | PERF | not_exact_due_to_execution_failure | candidate_execution_failed | false | not_eligible |
| spark | PORT_0003 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| spark | PORT_0004 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| spark | PORT_0005 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| spark | PORT_0008 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| spark | PORT_0012 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| spark | PORT_0013 | PORT | not_exact_due_to_execution_failure | candidate_execution_failed | false | not_eligible |
| spark | PORT_0022 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |
| spark | PORT_0024 | PORT | not_exact_due_to_execution_failure | unsupported_engine | false | not_eligible |
| spark | PORT_0025 | PORT | not_evaluated_non_db_mvp | no_candidate_sql | false | not_eligible |

Exact but not timed row copied from canonical timing output:

| Engine | Case | Pool | Exact status | Timing status | Exclusion reason |
| --- | --- | --- | --- | --- | --- |
| postgres | PORT_0024 | PORT | exact | not_eligible | timing_not_eligible |
