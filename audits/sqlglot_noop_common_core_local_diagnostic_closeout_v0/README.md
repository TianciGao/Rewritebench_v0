# SQLGlot Noop Common-core Local Diagnostic Closeout

Verdict: `closed_with_fail_visible_limitations`.

This packet closes the current Common-core SQLGlot noop user-entry local diagnostic sequence after the Spark statement-boundary patch and Spark-only rerun.

The route under closeout is:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

This is local diagnostic evidence only. It is not official SQLGlot baseline evidence, not a paper result, not a timing/speedup run, not retained-evidence promotion, not reports/results migration, and not a leaderboard.

## Current Engine Status

PostgreSQL current snapshot comes from `common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0`:

- selected rows: 40
- generated/preflight rows: 35/35
- source/candidate/checker rows: 35/35/35
- exact/mismatch rows: 35/0
- remaining failures: 5 PORT SQLGlot noop adapter parse/emit failures before candidate generation

MySQL current snapshot comes from `common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0`:

- selected rows: 40
- generated/preflight rows: 40/40
- source/candidate/checker rows: 40/39/39
- exact/mismatch rows: 31/8
- remaining failures: one PORT candidate execution failure, three PORT real-adapter semantic mismatches, and five label-only checker/normalization candidates including `PERF_0062`

Spark current snapshot is updated by `common_core_spark_sqlglot_noop_after_statement_patch_v0`:

- selected rows: 40
- generated/preflight rows: 40/40
- source/candidate/checker rows: 35/33/33
- exact/mismatch rows: 31/2
- non-PORT same-engine Spark rows: exact 31/31
- remaining failures: four PORT SQLGlot noop real-adapter rows and five explicit unsupported/fail-closed Spark PORT roles

## Spark Closeout

Spark non-PORT same-engine rows are now clean for this SQLGlot noop local diagnostic surface: exact `31/31`.

The six prior statement-boundary false failures are now exact:

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0082`

Remaining Spark failures are PORT-only or explicit unsupported/fail-closed rows.

## Combined Current Funnel

Combining the current PostgreSQL and MySQL snapshots from the original tri-engine run with the updated Spark snapshot:

- selected rows: 120
- candidate generated rows: 115
- candidate preflight passed rows: 115
- source executable rows: 110
- candidate executable rows: 107
- checker attempted rows: 107
- exact rows: 97
- mismatch rows: 10
- source-like/no-op rows: 6
- unsupported/fail-closed rows: 5

Failure buckets: `adapter_failed=5`, `candidate_execution_failed=3`, `mismatch=10`, `none=97`, `unsupported_engine=5`.

## Remaining Work

The remaining rows should stay fail-visible unless separately authorized:

- MySQL label-policy triage for `PERF_0062` and related label-only rows.
- SQLGlot noop PORT limitation documentation covering parse/emit failures and literalized identifier behavior.
- A separately named target-aware SQLGlot route design, if changing route semantics is desired.

Do not merge SQLGlot noop with SQLGlot optimize outcomes, controlled PORT target-reference diagnostics, timing, official metrics, or paper/reporting surfaces.
