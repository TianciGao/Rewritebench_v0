# External Schema Resolution Tests

## Implemented Behavior

`src/sql_rewrite_bench/postgres_execution.py` now resolves PostgreSQL executable schema assets with this order:

1. Load the case manifest at `cases/<POOL>/<CASE_ID>/manifest.yaml`.
2. Read `schema.external_profile`.
3. Resolve the external schema profile as a repository-relative path.
4. Read `engines.postgres.ddl` and `engines.postgres.load` from the external schema profile.
5. Resolve both DDL/load paths as repository-relative paths.
6. Fail closed if any field or path is missing, absolute, parent-relative, outside the repository, malformed, or nonexistent.

The code does not silently fall back to case-local `schema/postgres/ddl.sql` or `schema/postgres/load.sql`.

## Tests Added

- `test_smoke_selects_deterministic_tiny_subset`
- `test_smoke_rejects_case_list_and_pool_filters`
- `test_public_smoke_noop_adapter_writes_only_runs_user`
- `test_postgres_schema_resolution_uses_external_profile`
- `test_postgres_schema_resolution_fails_closed_without_external_profile`
- `test_db_execution_fails_closed_when_external_schema_metadata_missing`

## Validation Result

User-entry unit tests passed: 33 tests run, 1 skipped.

Live PostgreSQL DB/checker execution was not run. The external-schema compatibility was validated with static resolver and fail-closed unit tests.
