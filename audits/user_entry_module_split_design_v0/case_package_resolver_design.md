# Case Package Resolver Design

## Purpose

`case_package_resolver.py` should centralize package-asset resolution for a selected case-engine row. It exists so `user_run.py`, adapter invocation, optional DB execution, checker diagnostics, and future tag slices do not each rediscover case paths independently.

The resolver must fail closed when required package files are missing or unsafe. It must not invoke adapters, execute DB queries, run checkers, compute metrics, update reports/results, or create leaderboard rows.

## Input Fields

The minimal resolver call should accept:

- `repo_root: Path`
- `selected_row: SelectedCaseEngineRow`
- optional `require_reference_sql: bool = False`
- optional `require_checker_paths: bool = False`
- optional `require_validation_paths: bool = False`

The selected row remains owned by `case_selection.py` and provides:

- `case_id`
- `pool`
- `engine`
- `case_path`
- `source_sql_path`
- `denominator_id`
- `planned`

## Output Object Fields

Design-only interface: `ResolvedCasePackage`.

Required now:

- `case_id`
- `pool`
- `engine`
- `case_dir`
- `manifest_path`
- `source_sql_path`
- `schema_profile_path`
- `schema_external_profile_path`
- `checker_config_path`
- `normalization_config_path`
- `compare_config_path`
- `expected_rejections_path`
- `package_path_from_manifest`
- `manifest_schema`
- `manifest_taxonomy`
- `resolution_status`
- `resolution_notes`

Useful future fields:

- `positive_sql_path`
- `negative_sql_path`
- `validation_run_validation_path`
- `validation_run_plan_collection_path`
- `validation_run_engine_queries_path`
- `dialect_variant_paths`
- `tag_axes`
- `tag_values`
- `source_family`
- `source_workload`
- `source_query_identity`
- `known_caveats`

## Fail-Closed Conditions

The resolver should fail closed for:

- `case_dir` missing or escaping the repository root.
- `manifest.yaml` missing.
- `sql/source.sql` missing or not matching the selected row source path.
- `schema/schema_profile.yaml` missing.
- `schema.external_profile` absent from manifest when DB/checker diagnostics need schema resolution.
- Manifest `schema.external_profile` absolute, contains `..`, escapes repo root, or points to a missing file.
- Required checker config path missing when checker diagnostics are enabled.
- Required reference SQL path missing when a future phase explicitly requires it.
- Manifest `case_id`, `pool`, or `package_path` conflicts with selected row metadata.

The resolver should return a structured failure for ledger accounting rather than raising unhandled exceptions after implementation.

## Interaction With `case_selection.py`

`case_selection.py` remains the only owner of membership and denominator row selection. The resolver must not scan `cases/` to decide Common-core membership and must not read `case_sets/` to override a selected row.

The intended sequence is:

```text
case_selection.py -> SelectedCaseEngineRow -> case_package_resolver.py -> ResolvedCasePackage
```

## Interaction With Future Tag Slicing

Future `tag_slices.py` should consume taxonomy/tag fields exposed by the resolver. Tags must be read from manifest/taxonomy metadata, not inferred from SQL text at runtime.

The resolver may expose tags as raw manifest structures in the minimal split and normalize them later when tag-slice schema is authorized.

## Interaction With Engine Execution

For the minimal split, PostgreSQL execution may keep its existing external-schema resolver internally. A later engine-router phase should reuse `ResolvedCasePackage.schema_external_profile_path` to avoid duplicate manifest parsing.

The resolver does not open database connections and does not create execution artifacts.

## Non-Goals

- Adapter subprocess invocation.
- Candidate SQL capture.
- Candidate preflight.
- PostgreSQL/MySQL/Spark execution.
- Local result checking.
- Failure-bucket priority.
- Quality reports.
- Tag score or ranking.
- Timing diagnostics.
- Official metrics or paper rendering.
