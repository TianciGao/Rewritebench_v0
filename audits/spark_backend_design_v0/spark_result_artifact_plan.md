# Spark Result Artifact Plan

## Proposed Layout

For same-engine Spark diagnostics, write artifacts under the per-row workspace only:

```text
workspaces/<CASE_ID>/spark/execution/spark_same_engine/
  source_query.sql
  candidate_query.sql
  source_result.jsonl
  candidate_result.jsonl
  source_error.txt
  candidate_error.txt
  spark_execution_metadata.json
```

For future cross-dialect Spark roles, use distinct role directories such as `spark_source_reference/` or `spark_target_candidate/` so audits can tell same-engine and cross-dialect artifacts apart.

## JSONL Shape

`local_result_checker.py` currently expects each JSONL line to be one JSON object. Spark should export the same shape:

```json
{"col_a": 1, "col_b": "value", "col_c": null}
```

The key order in the serialized object should follow Spark DataFrame column order. The backend should build ordinary Python dictionaries in that order before JSON serialization, preserving insertion order for checker positional comparison in future cross-dialect contexts.

## Type Serialization Policy

Use JSON-native values where safe:

- integers -> JSON numbers
- floats/doubles -> JSON numbers, unless precision requires string preservation
- decimals -> strings preserving Spark decimal text representation
- strings -> JSON strings
- dates -> ISO `YYYY-MM-DD` strings
- timestamps -> ISO string with explicit timezone policy documented before live implementation; avoid implicit local timezone conversion
- booleans -> JSON booleans
- NULL -> JSON null
- arrays/structs/maps -> stable JSON arrays/objects only if present; otherwise fail closed as `spark_result_export_failed` until tests define the policy

Do not add broad date/time, boolean, NULL, or complex-type normalization in the checker as part of Spark execution. Export should be deterministic and explicit.

## Row Ordering

Spark result ordering is not guaranteed unless the SQL query includes `ORDER BY`. The first implementation should preserve the returned order and rely on existing checker compare/normalization config. It should not add new multiset logic or implicit sorting unless a later checker-policy task authorizes it.

## Metadata

`spark_execution_metadata.json` should record redacted local diagnostic metadata only:

- case id, pool, selected engine, diagnostic role
- Spark version and configured master if available
- schema external profile and Spark DDL/load paths
- namespace/database name
- source/candidate query artifact paths
- source/candidate result artifact paths
- row counts after export
- local-only boundary flags

Do not record passwords, full environment dumps, timing samples, speedup, official metric inputs, or reports/results paths.
