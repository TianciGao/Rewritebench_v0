# Track A 120 Readiness Impact

Current post-ARRAY_ANY bounded rerun:

- planned rows: 9
- exact/result-consistent rows: 6
- fail-closed rows: 1
- Spark mismatches: 2

## If CONS_0036 Label Normalization Is Authorized Later

If a future checker policy authorizes safe case-only label normalization and a rerun confirms the same value-exact condition:

- bounded exact rows could move from 6 to 7;
- bounded mismatch rows could move from 2 to 1;
- Spark exact rows could move from 1/3 to 2/3.

This would not resolve `CONS_0005` / Spark.

## Remaining Full-120 Blocker

`CONS_0005` / Spark still blocks full 40 x 3 readiness because it is a value/row-count semantic mismatch, not a label-only or formatting issue.

## Timing Readiness

Exact-gated timing is safe only over the current six exact rows:

- PostgreSQL: `CONS_0005`, `PERF_0006`, `CONS_0036`
- MySQL: `PERF_0006`, `CONS_0036`
- Spark: `PERF_0006`

Do not time:

- `CONS_0005` / MySQL fail-closed row;
- `CONS_0005` / Spark semantic mismatch;
- `CONS_0036` / Spark strict-label mismatch unless a future policy changes its exact classification.

## Full Track A 120 Readiness

`sqlglot_optimize_schema_aware` remains partial and is not ready for full Track A 120 local diagnostic rerun.

Recommended next options:

1. Authorize a narrow Spark label-normalization policy task for `CONS_0036`-style case-only labels.
2. Keep the route partial and run exact-gated timing over the six current exact rows.
3. Move to the SQLGlot noop Track A 120 rerun candidate while schema-aware optimize remains under development.
