# Future Prompt: PERF_0006 Canonical-Layout Full Case Migration

Do not execute this prompt during the planning task.

## Task

Perform a one-case copy-first canonical-layout full case migration for `PERF_0006` from the legacy repo into the release repo.

This is NOT Common-core 40 migration, batch migration, DB validation, evidence regeneration, deletion, cleanup, speedup recomputation, or authorization to mutate legacy files.

## Hard Boundaries

- Do not modify anything under the legacy repo.
- Do not run DB engines, validation scripts, LLM calls, timing workloads, or evidence regeneration.
- Do not change denominator, paper results, case membership, admission status, or case-set files.
- Do not create new speedup, timing, performance ranking, or global leaderboard claims.
- Do not copy raw `runs/` wholesale.
- Do not publish raw Spark plan text files with local temporary path traces.
- Do not use `git add .`.

## Read First

Read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `repository_spec/canonical_case_package_layout_v1.md`
- `repository_spec/static_case_package_validator_v0_3.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_canonical_layout_plan.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_canonical_file_mapping.csv`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_abort_conditions.md`
- `audits/canonical_layout_planning/PERF_0006/PERF_0006_performance_evidence_boundary_preview.md`

## Files To Create

Create canonical `cases/PERF/PERF_0006/` with:

- root `README.md` and generated `manifest.yaml`;
- `sql/source.sql`, `sql/positives/pos_01.sql`, and `sql/negatives/neg_01.sql`;
- engine DDL/load files under `schema/<engine>/`;
- `schema/schema_profile.yaml`, `data/data_profile.yaml`, and `data/witness_profile.yaml`;
- `checker/checker.yaml`, `checker/normalization.yaml`, `checker/compare_config.yaml`, and `checker/expected_rejections.yaml`;
- validation scripts as retained legacy validation assets with output-policy caveats;
- retained public evidence under `evidence/`;
- generated `metadata/*.yaml`;
- generated migration, risk, and witness notes.

## Source-To-Target Mapping Rules

- Copy `source.sql` to `sql/source.sql`.
- Copy `rewrite_pos_01.sql` to `sql/positives/pos_01.sql`.
- Copy `rewrite_neg_01.sql` to `sql/negatives/neg_01.sql` and document it as a hard negative because it excludes the cutoff-date row.
- Copy `schema/ddl_pg.sql`, `schema/ddl_mysql.sql`, and `schema/ddl_spark.sql` to `schema/postgres/ddl.sql`, `schema/mysql/ddl.sql`, and `schema/spark/ddl.sql`.
- Copy witness SQL files to `schema/<engine>/load.sql`.
- Generate checker YAML from retained checker and result evidence.
- Promote public-safe result-check, TSV, and JSON plan artifacts into `evidence/`.
- Sanitize Spark plan text files before any public retained copy, or keep them private/archive-only.
- Generate `evidence/runs_retention.yaml` mapping every retained original with `do_not_delete_original: true`.

## Performance Evidence Boundary

The actual migration must record:

- no timing artifacts were found in the case directory by planning inspection;
- no new speedup claim is created;
- correctness-gated performance remains tied to existing denominator-aware paper evidence;
- retained plan evidence is observability evidence, not timing evidence.

## Validation Commands

Run static checks only:

```bash
python -m py_compile scripts/dev/validate_case_package.py
python scripts/dev/validate_case_package.py --mode full-case --case cases/PERF/PERF_0006 --out audits/full_case_migration_pilots/PERF_0006_validator_full_case_result.csv
python scripts/dev/validate_case_package.py --mode canonical-case --case cases/PERF/PERF_0006 --out audits/full_case_migration_pilots/PERF_0006_validator_canonical_case_result.csv
git diff --stat
git diff --check
git status -sb
```

Also run SHA256 copy validation, public hygiene scan, YAML parse validation, and JSON parse validation.

## Commit Rules

Use explicit paths only. Do not use `git add .`.

Commit message:

```bash
git commit -m "pilot: canonical-layout migrate PERF_0006 case package"
```

Push:

```bash
git push origin main
```

## Final Response Format

Report legacy modification status, files created/modified, migration scope, denominator/paper/case-membership impact, raw legacy evidence impact, performance-boundary handling, plan evidence handling, Spark plan sanitization status, validator results, commit hash, push result, raw GitHub URLs, and exact next safe action.
