# Route Assembly Execution Review

The D035 user facade evaluated `common_core_v0` over `postgres,mysql,spark` with run id prefix `direct_llm_repair_1_track_a_120_canonical_v0`.

Route assembly summary:

- selected planned rows: 120
- original exact rows replayed as original final candidates: 102
- repair attempted rows: 13
- unsupported rows excluded from Repair-1 attempts: 5
- final candidate source `original`: 102
- final candidate source `repaired`: 13
- final candidate source `unsupported_or_none`: 5
- final candidate source `fail_closed`: 0
- live call count: 13
- fail-closed rows after route assembly: 0

The unsupported rows used preserved original candidate artifacts only to let the user facade reach the unsupported diagnostic path and record `unsupported_engine`. No live Repair-1 call was made for those rows.

Final ledger failure buckets:

```text
{'mismatch': 4, 'none': 111, 'unsupported_engine': 5}
```

Final exact-status counts:

```text
{'exact': 111, 'mismatch': 4, 'not_exact_due_to_execution_failure': 5}
```
