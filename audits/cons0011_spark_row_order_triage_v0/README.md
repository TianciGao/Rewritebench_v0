# CONS_0011 Spark Row-Order Triage v0

Verdict: `case_level_compare_config_gap`

## Summary

This packet triages the sole mismatch from the Common-core Spark local diagnostic run for `CONS_0011`.

The accepted local artifacts are from `runs/user/common_core_spark_noop_db_checker/`. No `CONS_0011` rerun was needed. The no-op adapter emitted source-like SQL, and the Spark execution workspace shows identical source and candidate SQL for this row. Spark returned the same two result values in different orders:

- source result: `ALICE`, `BOB`
- candidate result: `BOB`, `ALICE`

Both artifacts have two rows, the same `ENAME` column, and the same values after row sorting. Neither `cases/CONS/CONS_0011/sql/source.sql` nor `cases/CONS/CONS_0011/sql/pos_01.sql` contains `ORDER BY`, and the README/manifest do not state that visible row order is part of the semantic property. The case-local `compare_config.yaml` declares `semantic_equivalence` but does not declare a row-order policy. The local checker currently preserves row order unless `checker/normalization.yaml` has a recognized top-level `sort_rows: true`; `CONS_0011` does not declare that setting.

The mismatch is therefore not evidence of a true semantic mismatch. It is a case-level order policy/configuration gap surfaced by Spark row-order nondeterminism for an unordered query shape.

## Recommended Next Safe Action

Authorize a narrow future fix for `CONS_0011` only: make the case-local checker policy explicitly order-insensitive for this unordered semantic-equivalence comparison, using the repository-supported configuration path. Because the current checker reads `sort_rows` from `checker/normalization.yaml`, the fix should either use that supported setting or, if maintainers decide the policy belongs in `compare_config.yaml`, include a separately authorized checker-support change plus representative regression checks.

Regression protection should include `CONS_0011`, the prior two-case Spark smoke subset, representative PERF/CONS/LONGTAIL same-engine rows, and at least one hard-negative/control path where row order must not mask real value or row-count differences.

## Local-Only Boundary

This triage is local diagnostic/audit work only. It is not official metrics, not paper evidence, not timing or speedup, not reports/results migration, not retained evidence promotion, and not a leaderboard.

No checker behavior, source code, SQL file, manifest, case package, checker config, `case_sets/`, reports/results file, denominator, paper result, case membership, raw retained evidence, release tag, or export branch was changed.
