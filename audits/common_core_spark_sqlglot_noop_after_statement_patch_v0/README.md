# Common-core Spark SQLGlot Noop After Statement Patch

Verdict: `completed_with_remaining_port_failures`.

This packet records a Spark-only Common-core v0 local diagnostic snapshot after commit `b62c41c` using:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

Scope:

- Engine selected: Spark only.
- Case set: `common_core_v0`.
- Route: SQLGlot noop only.
- SQLGlot optimize: not run.
- Timing/speedup: not run.
- Official metrics: not computed.
- Reports/results: not updated.
- Retained evidence: not promoted.
- Leaderboard: not created.

## Aggregate Comparison

Previous Spark SQLGlot noop snapshot:

- selected rows: 40
- candidate generated/preflight passed rows: 40/40
- source/candidate/checker rows: 35/27/27
- exact rows: 25
- mismatch rows: 2
- failure buckets: `candidate_execution_failed=8`, `mismatch=2`, `none=25`, `unsupported_engine=5`

After statement-boundary patch:

- selected rows: 40
- candidate generated/preflight passed rows: 40/40
- source/candidate/checker rows: 35/33/33
- exact rows: 31
- mismatch rows: 2
- failure buckets: `candidate_execution_failed=2`, `mismatch=2`, `none=31`, `unsupported_engine=5`

The six rows from `spark_sqlglot_noop_statement_preflight_triage_v0` no longer fail with `Spark diagnostic query must contain exactly one statement`:

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0082`

Each now reaches source execution, candidate execution, checker, and exact status.

## Remaining Failures

Remaining fail-visible rows are all PORT rows:

- `PORT_0003`: candidate execution failed; SQLGlot noop emitted a Spark target candidate that tries to cast literal `'longitude'` to a number.
- `PORT_0013`: candidate execution failed; SQLGlot noop emitted a MySQL-style boolean aggregate not accepted by Spark.
- `PORT_0004`: checker mismatch; candidate returned `NULL` where the source reference returned a value.
- `PORT_0005`: checker mismatch; candidate returned literal `nationality` where the source reference returned `japan_earliest`.
- `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, `PORT_0025`: explicit Spark unsupported/fail-closed roles with `spark_target_reference_not_declared`.

These are local diagnostic user-adapter outcomes, not official SQLGlot baseline evidence or paper results.

## Metadata Correction

Preflight found that the previous `spark_statement_boundary_comment_aware_patch_v0` run-log entry still recorded commit hash and push result as pending. This packet records the non-destructive correction:

- Prior task final commit: `b62c41c`
- Prior task push result: pushed to `origin/feature/case-package-v2-external-schema`

## Local Run Path

`runs/user/common_core_spark_sqlglot_noop_after_statement_patch`

The run output remains local and is not committed.

## Next Safe Action

Keep the remaining PORT SQLGlot noop failures fail-visible, or separately authorize PORT real-adapter route/dialect triage. Do not mix these rows with controlled target-reference PORT diagnostics or official metric surfaces.
