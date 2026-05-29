# Known Policy Rows

Target-dialect guard:

- The MySQL/Spark PostgreSQL-dialect guard remained active.
- No MySQL/Spark row in this run was blocked by that guard.
- MySQL/Spark generated candidates used target dialect mode sufficiently to
  pass the guard.

Schema-fallback / parse-only output:

- `calcite_parse_only` candidate origin occurred in 41 rows overall:
  - PostgreSQL: 4
  - MySQL: 8
  - Spark: 29
- Parse-only rows are preserved in `per_row_execution_checker_status.csv` under
  `candidate_origin`.

DATETIME/TIMESTAMP and PORT blockers:

- Seven PORT cases remained no-candidate on every engine:
  `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`,
  `PORT_0022`, `PORT_0025`.
- `PORT_0013` generated parse-only candidates but failed candidate execution on
  PostgreSQL and Spark, and mismatched on MySQL.
- `PORT_0024` was exact on PostgreSQL, mismatched on MySQL, and unsupported on
  Spark due target-reference/source-role policy.

Checker policy:

- No checker normalization or label policy was changed.
- Strict mismatches remain mismatches.
