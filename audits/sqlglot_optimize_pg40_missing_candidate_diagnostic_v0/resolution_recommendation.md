# Resolution Recommendation

## Per-Case Classification

- `CONS_0009`: `rerun_sqlglot_optimize_candidate_capture_needed`. Current evidence is a SQLGlot optimize generation/adapter failure, not a path-only or manifest-only issue. Keep the row missing until actual optimize candidate SQL is produced for PostgreSQL.
- `PORT_0004`: `rerun_sqlglot_optimize_candidate_capture_needed`. Current evidence is a SQLGlot optimize generation/adapter failure, not a path-only or manifest-only issue. Keep the row missing until actual optimize candidate SQL is produced for PostgreSQL.
- `PORT_0013`: `rerun_sqlglot_optimize_candidate_capture_needed`. Current evidence is a SQLGlot optimize generation/adapter failure, not a path-only or manifest-only issue. Keep the row missing until actual optimize candidate SQL is produced for PostgreSQL.
- `PORT_0022`: `rerun_sqlglot_optimize_candidate_capture_needed`. Current evidence is a SQLGlot optimize generation/adapter failure, not a path-only or manifest-only issue. Keep the row missing until actual optimize candidate SQL is produced for PostgreSQL.
- `PORT_0024`: `rerun_sqlglot_optimize_candidate_capture_needed`. Current evidence is a SQLGlot optimize generation/adapter failure, not a path-only or manifest-only issue. Keep the row missing until actual optimize candidate SQL is produced for PostgreSQL.
- `PORT_0025`: `rerun_sqlglot_optimize_candidate_capture_needed`. Current evidence is a SQLGlot optimize generation/adapter failure, not a path-only or manifest-only issue. Keep the row missing until actual optimize candidate SQL is produced for PostgreSQL.

## Route-Level Recommendation

SQLGlot optimize schema-aware PostgreSQL is not full-PG40 ready after this diagnostic. The current state is `partial34_only`: 34 candidate-present rows and 6 manifest-visible generation failures.

It cannot be made 40/40 by fixing a manifest/path mapping alone. A later authorized SQLGlot optimize candidate-capture rerun or adapter/parser fix is needed to produce actual SQLGlot optimize PostgreSQL candidate SQL for the missing cases.

A partial 34/40 POCR diagnostic could be separately authorized only if the missing rows remain visible as fail-closed/skipped candidate rows and the scope is explicitly labeled partial. That would not be a full PG40 diagnostic.

If the team wants the next complete deterministic diagnostic baseline instead, switch to SQLGlot no-op sanity/control as a separate route; do not use no-op files to fill SQLGlot optimize rows.
