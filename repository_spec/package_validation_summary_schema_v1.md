# Package Validation Summary Schema v1

Status: schema guard for case-local `evidence/package_validation_summary.json`

## Purpose

`evidence/package_validation_summary.json` is a case-local summary of package validation, public hygiene, retained-evidence indexing, and claim boundaries. It is not a repository construction run log and must not duplicate task-level audit or project-control fields.

## Allowed Case-local Fields

Future package summaries should prefer fields in these groups:

- `case_id`
- `pool`
- `summary_type`
- `canonical_layout_status`
- `validation_scope`
- `static_validation_status`
- `public_hygiene_status`
- `retained_evidence_index_status`
- `sql_asset_status`
- `schema_asset_status`
- `checker_asset_status`
- `validation_asset_status`
- `metadata_asset_status`
- `known_local_package_caveats`
- `claim_boundaries`

Allowed `claim_boundaries` keys include local package claims such as:

- `db_validation_run`
- `evidence_regenerated`
- `metrics_computed`
- `paper_tables_rendered`
- `leaderboard_created`
- `new_runtime_outputs_created`

## Discouraged Or Task-level Fields

The following fields belong in `audits/` or `project_control/`, not in case-local package summaries:

- `denominator_changed`
- `paper_results_changed`
- `raw_legacy_evidence_changed`
- `reports_changed`
- `results_changed`
- `case_sets_changed`
- commit hashes
- push results
- agent or task metadata
- batch identifiers
- repository run-log status
- construction-process dates unrelated to intrinsic package validation

## Valid Case-local Example

```json
{
  "case_id": "PERF_0006",
  "pool": "PERF",
  "summary_type": "case_package_validation_summary",
  "canonical_layout_status": "pass",
  "validation_scope": "static_package_validation_only",
  "static_validation_status": "pass",
  "public_hygiene_status": "pass",
  "retained_evidence_index_status": "present",
  "sql_asset_status": "present",
  "schema_asset_status": "present",
  "checker_asset_status": "present",
  "validation_asset_status": "present",
  "metadata_asset_status": "present",
  "known_local_package_caveats": [],
  "claim_boundaries": {
    "db_validation_run": false,
    "evidence_regenerated": false,
    "metrics_computed": false,
    "paper_tables_rendered": false,
    "leaderboard_created": false,
    "new_runtime_outputs_created": false
  }
}
```

## Fields That Must Stay In Audits Or Project Control

Repository-wide mutation claims, commit/push outcomes, batch names, and policy decisions belong in task audit outputs and `project_control/MIGRATION_RUN_LOG.md`. They should not be copied into case-local summaries.

## Guidance For Wave 002 Package Generation

Wave 002 package generation should create package summaries that follow this guard. If repository-wide boundaries need to be recorded, place them in the wave audit summary and project-control files instead. Case summaries should remain intrinsic to the case package.

## Backward Compatibility

Existing package summaries may contain legacy construction-process fields. This schema guard does not rewrite them automatically. Existing files should be audited first, then normalized by a separate bounded package-summary normalization task if the maintainer authorizes it.
