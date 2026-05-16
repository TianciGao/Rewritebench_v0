# Future Prompt: LONGTAIL_0011 Canonical-Layout Full Case Migration Pilot

This prompt is a draft for a future task. Do not execute it during the planning task.

## Task

You are working on SQL-RewriteBench clean public release migration.

Current repository roles:

- Legacy/source repository: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
- New public release repository: `/home/tianci_gao/code/Rewritebench_v0`

Task title: `LONGTAIL_0011 canonical-layout full case migration pilot`

This is a one-case copy-first canonical-layout full case migration pilot. It is not Common-core 40 migration, not batch migration, not DB validation, not evidence regeneration, and not authorization to delete or mutate legacy files.

Selected case: `LONGTAIL_0011`

Reason: `LONGTAIL_0011` tests canonical layout for realistic, structurally complex, long-tail SQL. It is SQLStorm/StackOverflow-derived, uses CTE and window-function structure, and has a tie-handling hard negative.

## Read First

Read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `repository_spec/canonical_case_package_layout_v1.md`
- `repository_spec/case_package_contract_v1.md`
- `repository_spec/runs_retention_policy_v1.md`
- `repository_spec/static_case_package_validator_v0_3.md`
- `scripts/dev/validate_case_package.py`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_canonical_layout_plan.md`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_proposed_canonical_tree.txt`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_manifest_preview.yaml`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_runs_retention_after_canonical_preview.yaml`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_longtail_structure_boundary_preview.md`
- `audits/canonical_layout_planning/LONGTAIL_0011/LONGTAIL_0011_abort_conditions.md`

Confirm:

- `PORT_0004`, `PORT_0008`, `CONS_0005`, and `PERF_0006` remain the only completed full-case pilots.
- `LONGTAIL_0011` is not yet migrated.
- Common-core 40 migration has not started.
- Denominator, paper results, case membership, and raw legacy evidence must not change.

## Hard Boundaries

Do not modify anything under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`.

Do not delete, move, rename, sanitize in place, overwrite, reset, clean, restore, pull, checkout, add, commit, or otherwise mutate the legacy repo.

Do not run DB engines, validation scripts, LLM calls, timing workloads, evidence regeneration, or plan regeneration.

Do not change Common-core membership, denominator, paper results, case admission status, `case_sets/`, or `reports/evaluation/common_core_v0/`.

Do not use `git add .`.

Allowed writes are only under `/home/tianci_gao/code/Rewritebench_v0`.

## Legacy State Snapshot

Record the following read-only legacy state into the audit report:

- `pwd`
- `git branch --show-current`
- `git rev-parse HEAD`
- `git status -sb`
- `git diff --name-status`
- `git log --oneline -3`

## Canonical Target

Create:

`cases/LONGTAIL/LONGTAIL_0011/`

Create the canonical layout:

- `README.md`
- `manifest.yaml`
- `sql/source.sql`
- `sql/positives/pos_01.sql`
- `sql/negatives/neg_01.sql`
- `schema/postgres/ddl.sql`
- `schema/postgres/load.sql`
- `schema/mysql/ddl.sql`
- `schema/mysql/load.sql`
- `schema/spark/ddl.sql`
- `schema/spark/load.sql`
- `schema/schema_profile.yaml`
- `data/data_profile.yaml`
- `data/witness_profile.yaml`
- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`
- `checker/expected_rejections.yaml`
- `validation/run_postgres_validation.sh`
- `validation/run_mysql_validation.sh`
- `validation/run_spark_validation.sh`
- `validation/run_postgres_plan_collection.sh`
- `validation/run_mysql_plan_collection.sh`
- `validation/run_spark_plan_collection.sh`
- `evidence/runs_retention.yaml`
- `evidence/retained_controls/`
- `evidence/retained_plans/`
- `evidence/hard_negative/`
- `evidence/package_validation_summary.json`
- `metadata/provenance.yaml`
- `metadata/taxonomy.yaml`
- `metadata/engine_support.yaml`
- `metadata/denominator_eligibility.yaml`
- `metadata/artifact_paths.yaml`
- `notes/witness_design_notes.md`
- `notes/risk_notes.md`
- `notes/schema_notes.md`
- `notes/promotion_checklist.md`
- `notes/migration_notes.md`

Do not copy raw `runs/` wholesale. Do not create public raw `runs/` unless a placeholder README is needed.

## Mapping Rules

Use `LONGTAIL_0011_canonical_file_mapping.csv` as the source-to-target map.

Copy and rename SQL, schema, witness-load files, selected notes, validation assets, result TSVs, result summaries, and public-safe PostgreSQL/MySQL JSON plans.

Generate canonical README, manifest, checker YAML, expected-rejection YAML, schema/data profiles, metadata YAML, package summary JSON, migration notes, and runs-retention YAML.

Hard-negative checker reason:

- `hard_negative_id: neg_01`
- `expected_rejection_reason: tie_handling_semantics_changed`
- `semantic_risk_type: [rank_function_substitution, dense_rank_to_row_number, tie_collapse]`
- `checker_guard_role: source_positive_equal_and_negative_differs_on_tie_bearing_witness`
- `observed_static_basis`: source/positive retain both Alice worst-score ties; negative collapses the tie to one Alice row.
- `approval_status`: `needs_human_review_before_actual_migration` unless a maintainer explicitly approves the exact reason string.

## Spark Plan Handling

Do not copy raw Spark plan text files into public retained evidence.

Sanitize before public copy:

- `runs/spark/plans/source.txt` -> `evidence/retained_plans/spark/source.sanitized.txt`
- `runs/spark/plans/rewrite_pos_01.txt` -> `evidence/retained_plans/spark/rewrite_pos_01.sanitized.txt`
- `runs/spark/plans/rewrite_neg_01.txt` -> `evidence/retained_plans/spark/rewrite_neg_01.sanitized.txt`

Replace `file:/tmp...` and `/tmp/...` with `<LOCAL_TMP_PATH_REDACTED>`. Replace other local absolute paths with `<LOCAL_PATH_REDACTED>`. Preserve plan structure and SQL semantics.

Map raw original Spark plan files in `evidence/runs_retention.yaml` with `do_not_delete_original: true` and `public_safe: false`.

## Validation Script Caveat

Copied validation scripts are retained legacy validation assets. They are not final public user runners, they must not be executed during migration, and future public runners should write outputs outside case-local `runs/` by default. Adapt WSL-local comment wording if needed to pass public hygiene.

## Validations To Run

Run:

```bash
python scripts/dev/validate_case_package.py --mode full-case --case cases/LONGTAIL/LONGTAIL_0011 --out audits/full_case_migration_pilots/LONGTAIL_0011_validator_full_case_result.csv
python scripts/dev/validate_case_package.py --mode canonical-case --case cases/LONGTAIL/LONGTAIL_0011 --out audits/full_case_migration_pilots/LONGTAIL_0011_validator_canonical_case_result.csv
python scripts/dev/validate_case_package.py --mode evidence-pilot --case cases/PORT/PORT_0008 --case cases/PORT/PORT_0012 --case cases/PORT/PORT_0013 --case cases/PORT/PORT_0022 --case cases/PORT/PORT_0025 --case cases/PORT/PORT_0024 --out audits/full_case_migration_pilots/LONGTAIL_0011_evidence_pilot_regression_result.csv
python scripts/dev/validate_case_package.py --mode full-case --case cases/PORT/PORT_0004 --case cases/PORT/PORT_0008 --case cases/CONS/CONS_0005 --case cases/PERF/PERF_0006 --out audits/full_case_migration_pilots/LONGTAIL_0011_full_case_regression_result.csv
python -m py_compile scripts/dev/validate_case_package.py
git diff --stat
git diff --check
git status -sb
```

Also run SHA256 copy validation, public hygiene scan, YAML parsing, and JSON parsing for the new package.

## Commit Rules

Use explicit paths only:

```bash
git add \
  cases/LONGTAIL/LONGTAIL_0011 \
  audits/full_case_migration_pilots/LONGTAIL_0011_canonical_full_case_migration_pilot.md \
  audits/full_case_migration_pilots/LONGTAIL_0011_canonical_full_case_file_inventory.csv \
  audits/full_case_migration_pilots/LONGTAIL_0011_canonical_full_case_validation.csv \
  audits/full_case_migration_pilots/LONGTAIL_0011_validator_full_case_result.csv \
  audits/full_case_migration_pilots/LONGTAIL_0011_validator_canonical_case_result.csv \
  audits/full_case_migration_pilots/LONGTAIL_0011_evidence_pilot_regression_result.csv \
  audits/full_case_migration_pilots/LONGTAIL_0011_full_case_regression_result.csv \
  project_control/MIGRATION_STATUS.md \
  project_control/MIGRATION_RUN_LOG.md
git commit -m "pilot: canonical-layout migrate LONGTAIL_0011 case package"
git push origin main
```

Do not use `git add .`.

## Final Response Format

Report legacy repo modification status, files created/modified in release repo, full-case migration scope, canonical layout result for LONGTAIL pool, denominator/paper/membership/raw evidence unchanged status, hard-negative/checker summary, Spark plan sanitization summary, validation summary, remaining risks, git diff summary, commit hash, push result, raw GitHub URLs, and exact next safe action.
