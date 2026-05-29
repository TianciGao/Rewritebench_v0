# CONS_0011 Order-Insensitive Policy Fix v0

Verdict: `completed`

## Summary

This packet records a narrow case-local checker policy fix for `CONS_0011`.

The prior triage under `audits/cons0011_spark_row_order_triage_v0/` found that the Spark local diagnostic mismatch was row-order-only: the source and candidate result artifacts contained the same two `ENAME` rows, `ALICE` and `BOB`, but in different order. Neither source nor positive SQL contains `ORDER BY`, and the case README/manifest do not declare visible row order as semantic.

The implementation adds top-level `sort_rows: true` to `cases/CONS/CONS_0011/checker/normalization.yaml` only. Existing normalization rules were preserved. No SQL files, manifests, global checker behavior, source code, or other case checker configs were changed.

## Validation Summary

`CONS_0011` Spark local diagnostic after the fix:

- selected rows: 1
- Spark source executable rows: 1
- Spark candidate executable rows: 1
- checker attempted rows: 1
- exact rows: 1
- mismatch rows: 0
- failure buckets: `none=1`

Prior two-case Spark smoke regression:

- selected rows: 2
- Spark source/candidate executable rows: 2/2
- checker attempted/exact/mismatch rows: 2/2/0
- failure buckets: `none=2`

Common-core Spark local diagnostic after the fix:

- selected rows: 40
- Spark source/candidate executable rows: 31/31
- checker attempted/exact/mismatch rows: 31/31/0
- failure buckets: `none=31`, `unsupported_engine=9`
- PORT Spark rows remained explicit unsupported/fail-closed.

Additional validation passed:

- `git diff --check`
- YAML parse check for `CONS_0011` normalization
- case-package v2 reference validator over all 40 Common-core cases
- `PYTHONPATH=src pytest tests/user_entry` with 118 passed and 1 skipped
- protected-surface checks

## Boundary

This is a case-local checker policy fix for local diagnostics only. It is not official metrics, not timing or speedup, not reports/results migration, not retained evidence promotion, not paper evidence, and not a leaderboard.

No denominator, paper result, case membership, raw retained evidence, release tag, or export branch was changed. Local run outputs under `runs/user/` are not committed.

## Recommended Next Safe Action

Use the fixed `CONS_0011` policy in future local Spark diagnostics. Any broader checker-policy migration, official metrics computation, timing/speedup work, reports/results update, retained-evidence promotion, or release export remains separately authorized work.
