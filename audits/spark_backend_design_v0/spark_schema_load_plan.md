# Spark Schema and Load Plan

## Resolution

Spark schema assets must be resolved from manifest metadata, not guessed:

1. Read the selected case manifest through `case_package_resolver.py`.
2. Read `schema.external_profile` from the manifest.
3. Load the external schema profile.
4. Require an `engines.spark` entry.
5. Resolve `engines.spark.ddl` and `engines.spark.load` as repository-relative paths.
6. Require both paths to exist before any Spark session executes SQL.

If any step fails, return `spark_schema_missing` or `spark_schema_setup_failed` as appropriate. Do not substitute PostgreSQL/MySQL DDL or load SQL.

## Expected Asset Types

Current external profiles use Spark SQL DDL and load SQL files, typically:

- `schemas/<schema_id>/spark/ddl.sql`
- `schemas/<schema_id>/spark/load.sql`

The first implementation should support SQL DDL/load statements only. CSV, parquet, temp-view fixture loaders, and DataFrame fixture builders should remain future work unless a later schema contract explicitly adds them.

## Per-Case Isolation

Use an isolated database or temp-view namespace per case-engine-row, derived from run id, case id, and engine. The namespace should be safe for Spark identifiers and should live in a per-run warehouse/scratch location under `runs/user/<run_id>/` or the per-row workspace. Cleanup should drop the temporary database/views and remove per-run scratch artifacts when safe.

## Loading Sequence

For same-engine Spark diagnostics:

1. Create or reset the per-case Spark database/namespace.
2. Execute Spark DDL.
3. Execute Spark load SQL.
4. Set the active database or qualify table names before source/candidate execution.
5. Execute source SQL and export `source_result.jsonl`.
6. Execute candidate SQL and export `candidate_result.jsonl`.
7. Return paths to the engine router.

For future cross-dialect Spark routes, use the manifest-declared source-reference and target-candidate roles; do not infer from filename or pool.

## Missing Schema Behavior

- Missing external profile: `spark_schema_missing`, failure bucket `source_execution_failed` for source side or `candidate_execution_failed` for target side.
- Missing `engines.spark`: `spark_schema_missing`.
- Missing Spark DDL/load path: `spark_schema_missing`.
- DDL/load execution error: `spark_schema_setup_failed`.

These are local diagnostic statuses only and not official metric classifications.
