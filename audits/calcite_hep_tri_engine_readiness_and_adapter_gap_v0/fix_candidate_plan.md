# Fix Candidate Plan

Implemented in this task:

- Added a narrow MySQL/Spark fail-closed guard in
  `baselines/calcite_hep_fail_closed/adapter.py`.
- The guard detects known PostgreSQL-dialect output forms for non-PostgreSQL
  targets:
  - double-quoted identifiers
  - `DOUBLE PRECISION`
- The guard blocks the candidate before DB execution and records
  `calcite_target_dialect_unsupported` plus an explicit bucket such as
  `mysql_postgres_dialect_quoted_identifier`.
- Focused tests cover MySQL and Spark guard behavior.

Safe next fix candidates:

1. Add or stage an external Calcite runtime engine-mode contract that can emit
   target dialect SQL for `postgres`, `mysql`, and `spark`.
2. Keep the adapter fail-closed unless the runtime explicitly reports or emits
   target-dialect-safe SQL.
3. Add focused MySQL/Spark smoke tests after any runtime engine-mode change.

Separate tasks that should not be mixed into this adapter guard:

- DATETIME/TIMESTAMP syntax and type handling.
- PORT source-role and cross-dialect policy.
- Schema-fallback execution policy.
- Checker label-normalization policy.
- Semantic mismatch triage.

Do not implement a broad SQL rewriter in the adapter. The next dialect fix
should be runtime/contract-level or a tightly scoped fail-closed check.
