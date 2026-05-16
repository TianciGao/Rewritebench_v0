# Future Prompt: CONS_0005 Canonical-Layout Full Case Migration

Do not execute this prompt during the planning task.

## Task

Perform a one-case copy-first canonical-layout full case migration for `CONS_0005` from the legacy repo into the release repo.

This is NOT Common-core 40 migration, batch migration, DB validation, evidence regeneration, deletion, cleanup, or authorization to mutate legacy files.

## Repositories

- Legacy/source repo: `/home/tianci_gao/code/sql-rewrite-bench-artifact-clean`
- Release repo: `/home/tianci_gao/code/Rewritebench_v0`

## Hard Boundaries

- Do not modify anything under the legacy repo.
- Do not run DB engines, validation scripts, LLM calls, timing workloads, or evidence regeneration.
- Do not change denominator, paper results, case membership, admission status, or case-set files.
- Do not copy raw `runs/` wholesale.
- Do not publish raw Spark plan text files with `file:/tmp` traces.
- Do not use `git add .`.

## Read First

Read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `repository_spec/canonical_case_package_layout_v1.md`
- `repository_spec/static_case_package_validator_v0_3.md`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_canonical_layout_plan.md`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/CONS_0005/CONS_0005_abort_conditions.md`

## Source-To-Target Rules

- Copy `source.sql` to `sql/source.sql`.
- Copy `rewrite_pos_01.sql` to `sql/positives/pos_01.sql`.
- Copy `rewrite_neg_01.sql` to `sql/negatives/neg_01.sql`.
- Copy `schema/ddl_pg.sql`, `schema/ddl_mysql.sql`, and `schema/ddl_spark.sql` to `schema/postgres/ddl.sql`, `schema/mysql/ddl.sql`, and `schema/spark/ddl.sql`.
- Copy witness SQL files to `schema/<engine>/load.sql`.
- Generate `schema/schema_profile.yaml`, `data/data_profile.yaml`, and `data/witness_profile.yaml`.
- Generate checker YAML files. Do not mark expected rejection complete unless human-approved.
- Generate or adapt validation scripts with canonical paths and output-policy caveats.
- Promote public-safe JSON and TSV retained evidence into `evidence/`.
- Sanitize Spark plan text files before any public retained copy, or keep them private/archive-only.
- Generate `manifest.yaml`, `README.md`, `metadata/*.yaml`, `notes/migration_notes.md`, `evidence/package_validation_summary.json`, and `evidence/runs_retention.yaml`.

## Checker Handling

`checker/expected_rejections.yaml` must encode `neg_01` as a hard negative for NULL-sensitive correlated `NOT IN` decorrelation. It must cite retained source, positive, and negative outputs and record approval status.

## Validation Commands

Run:

```bash
python -m py_compile scripts/dev/validate_case_package.py
python scripts/dev/validate_case_package.py --mode full-case --case cases/CONS/CONS_0005 --out audits/full_case_migration_pilots/CONS_0005_validator_full_case_result.csv
python scripts/dev/validate_case_package.py --mode canonical-case --case cases/CONS/CONS_0005 --out audits/full_case_migration_pilots/CONS_0005_validator_canonical_case_result.csv
git diff --stat
git diff --check
git status -sb
```

Also run SHA256 copy validation, public hygiene scan, YAML parse validation, and JSON parse validation.

## Commit Rules

Use explicit paths only. Do not use `git add .`.

Commit message:

```bash
git commit -m "pilot: canonical-layout migrate CONS_0005 case package"
```

Push:

```bash
git push origin main
```

## Final Response Format

Report legacy modification status, files created/modified, migration scope, denominator/paper/case-membership impact, raw legacy evidence impact, checker/hard-negative handling, Spark plan sanitization status, validator results, commit hash, push result, raw GitHub URLs, and exact next safe action.
