# Future Codex Prompt: Execute PORT_0008 Canonical-Layout Full Case Migration

Task title: PORT_0008 canonical-layout full case migration pilot

This prompt is a draft for a future task. Do not execute it during planning.

## Repository roles

- Legacy/source repository: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
- Public release repository: `/home/tianci_gao/code/Rewritebench_v0`

## Scope

Migrate `PORT_0008` only into the canonical case package layout. This is not Common-core 40 migration, not batch migration, not DB validation, not evidence regeneration, and not authorization to delete or mutate legacy files.

## Read first

Read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `repository_spec/canonical_case_package_layout_v1.md`
- `repository_spec/case_package_contract_v1.md`
- `repository_spec/runs_retention_policy_v1.md`
- `repository_spec/static_case_package_validator_v0_2.md`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_canonical_layout_plan.md`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/PORT_0008/PORT_0008_abort_conditions.md`

## Hard boundaries

Do not modify anything under `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`.

Do not run DB engines, validation scripts, LLM calls, timing workloads, or plan regeneration.

Do not change denominator, paper results, Common-core membership, case admission, case sets, or benchmark claims.

Do not copy raw Spark plan files into public retained evidence.

Do not use `git add .`.

## Required release outputs

Create/update only explicit `PORT_0008` canonical package paths under `cases/PORT/PORT_0008/`, plus audit outputs and project-control writeback.

Create canonical layout:

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
- `evidence/retained_controls/result_check.json`
- `evidence/retained_controls/pg_source.tsv`
- `evidence/retained_controls/mysql_rewrite_pos_01.tsv`
- `evidence/retained_controls/spark_rewrite_pos_01.tsv`
- `evidence/retained_plans/plan_check.json`
- `evidence/retained_plans/postgres/source.json`
- `evidence/retained_plans/mysql/rewrite_pos_01.json`
- `evidence/retained_plans/mysql/rewrite_neg_01.json`
- `evidence/retained_plans/rewrite_neg_01.sanitized.txt`
- `evidence/retained_plans/rewrite_pos_01.sanitized.txt`
- `evidence/hard_negative/mysql_rewrite_neg_01.tsv`
- `evidence/hard_negative/spark_rewrite_neg_01.tsv`
- `evidence/hard_negative/hard_negative_summary.json`
- `evidence/package_validation_summary.json`
- `metadata/provenance.yaml`
- `metadata/taxonomy.yaml`
- `metadata/engine_support.yaml`
- `metadata/denominator_eligibility.yaml`
- `metadata/artifact_paths.yaml`
- `notes/witness_design_notes.md`
- `notes/risk_notes.md`
- `notes/promotion_checklist.md`
- `notes/migration_notes.md`

## Mapping rules

Use `PORT_0008_canonical_file_mapping.csv` as the authoritative source-to-target map.

Copy SQL/DDL/load/TSV/JSON public-safe files byte-for-byte where marked `copy_and_rename`.

Generate manifest/checker/metadata/profile/summary files from the planning previews and retained evidence without changing scientific claims.

Reuse existing sanitized plan files. Verify SHA256 before and after.

Do not copy raw legacy Spark plan text files. Map them in `runs_retention.yaml` as do-not-delete original/private-or-archive references.

Do not copy raw `runs/` wholesale.

## Validation commands

Run:

```bash
python -m py_compile scripts/dev/validate_case_package.py
python scripts/dev/validate_case_package.py --mode full-case --case cases/PORT/PORT_0008 --out audits/full_case_migration_pilots/PORT_0008_validator_full_case_result.csv
python scripts/dev/validate_case_package.py --mode evidence-pilot --case cases/PORT/PORT_0008 --out audits/full_case_migration_pilots/PORT_0008_evidence_pilot_regression_result.csv
```

Also run YAML/JSON parse checks, SHA256 copy checks, and a public hygiene scan over `cases/PORT/PORT_0008`.

Abort on any condition listed in `PORT_0008_abort_conditions.md`.

## Commit rules

Stage explicit paths only. Do not use `git add .`.

Commit message:

```bash
git commit -m "pilot: canonical-layout migrate PORT_0008 case package"
```

Push:

```bash
git push origin main
```

## Final response requirements

Report legacy modification status, files created/modified, actual migration scope, denominator/paper/case-membership status, raw legacy evidence status, validation summary, sanitized evidence handling, git diff summary, commit hash, push result, raw URLs, and exact next safe action.
