# Pre/Post Guard Comparison

Input pre-guard diagnostic:

- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`

Guard implementation audit:

- `audits/sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0/`

## Aggregate Movement

| field | before guard | after guard |
|---|---:|---:|
| planned rows | 9 | 9 |
| generated executable candidates | 9 | 8 |
| preflight passed rows | 9 | 8 |
| fail-closed rows | 0 | 1 |
| source executable rows | 9 | 9 |
| candidate executable rows | 8 | 8 |
| checker attempted rows | 8 | 8 |
| exact/result-consistent rows | 6 | 6 |
| mismatch rows | 2 | 2 |
| source execution failures | 0 | 0 |
| candidate execution failures | 1 | 0 |

## Interpretation

The desired movement occurred:

- `CONS_0005` / MySQL moved from `candidate_execution_failed` to explicit fail-closed.
- Candidate execution failures dropped from 1 to 0.
- Fail-closed rows increased from 0 to 1.
- Exact and mismatch counts remained unchanged.
- PostgreSQL stayed 3/3 exact.
- MySQL stayed stable on the two executable rows.
- Spark blockers remained separate.

This is local diagnostic evidence only. It is not official metric input and is not paper-facing evidence.
