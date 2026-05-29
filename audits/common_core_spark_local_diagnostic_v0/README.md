# Common-core Spark Local Diagnostic v0

Verdict: `completed_with_failures`

## Summary

This packet records a bounded Common-core v0 Spark local diagnostic trial using `examples/user/noop_adapter.py`.

The accepted local run is `runs/user/common_core_spark_noop_db_checker/`. It selected 40 Spark rows, generated 40 candidates, passed candidate preflight for 40 rows, enabled DB execution for 40 rows, executed Spark source SQL for 31 rows, executed Spark candidate SQL for 31 rows, attempted the checker for 31 rows, and reached exact 30 with mismatch 1.

Failure bucket summary:

- `none=30`
- `mismatch=1`
- `unsupported_engine=9`

Diagnostic mode distribution:

- `same_engine=31`
- `unsupported=9`

The mismatch is `CONS_0011`, where source and candidate result artifacts contain the same two names in different order (`ALICE`, `BOB` versus `BOB`, `ALICE`). This is classified as a checker/normalization row-order issue for this local diagnostic run, not as official paper evidence.

The nine unsupported rows are all Common-core PORT cases. Their Spark local diagnostic role is explicitly fail-closed, so no Spark source SQL, target SQL, target-reference substitution, or checker fallback was attempted for those rows.

## Local-only Boundary

This run is local diagnostic output only. It is not official metrics, not paper results, not timing or speedup, not reports/results migration, not retained evidence promotion, and not a leaderboard input.

No official metrics were computed. No timing or speedup was computed. No `reports/` or `results/` files were updated. No Common-core membership, denominator, paper result, case package, SQL, schema, checker, validation, manifest, inventory, or raw retained evidence files were changed. No release tag or export branch was created.

The local run output under `runs/user/common_core_spark_noop_db_checker/` is ignored local diagnostic output and is not committed.

## Recommended Next Safe Action

Review the two local diagnostic failure classes before broader Spark work: keep PORT Spark roles fail-closed unless a separate Spark PORT role task is authorized, and investigate whether `CONS_0011` needs a narrow row-order normalization/checker policy update for Spark diagnostics. Any follow-up must remain local-only unless a separate metrics or reporting phase is authorized.
