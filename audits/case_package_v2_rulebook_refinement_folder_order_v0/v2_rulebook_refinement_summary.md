# Case Package v2 Rulebook Refinement Summary

Task: `case_package_v2_rulebook_refinement_folder_order_v0`

Branch: `feature/case-package-v2-external-schema`

## Purpose and Scope

This branch-only refinement updates the v2 plan before any additional writable case conversion. It records that future conversion should proceed by folder or asset layer rather than ad hoc per-case edits.

No case files, schema files, case sets, inventory, reports, results, denominators, paper results, retained evidence, DB/checker execution, official metrics, or leaderboard outputs were modified or created.

## Why Refinement Is Needed

The previous rulebook externalized executable DDL/load and minimized case-local schema assets. The batch dry-run showed that future reviewers still need a stable case-local schema summary while avoiding duplicated executable schema scripts. This refinement records the clean v2 compromise: keep only `schema/schema_profile.yaml` in each case and keep executable DDL/load under `schemas/<SCHEMA_ID>/<engine>/`.

## Schema Profile-only Policy

Clean v2 retains case-local `schema/` only for `schema/schema_profile.yaml`.

The profile is a case-facing summary and linkage file. It records `schema_id`, external schema profile, source family, relevant tables, columns, types, primary keys, foreign keys, dialect differences, fixture/data notes when needed, and engine support summary.

Executable DDL/load remain external under:

```text
schemas/<SCHEMA_ID>/<engine>/ddl.sql
schemas/<SCHEMA_ID>/<engine>/load.sql
```

Case-local per-engine DDL/load may remain only as compatibility artifacts until a separate cleanup task proves safe deletion.

## Shared Checker and Validator Module Plan

Case-local `checker/` remains configuration only:

- `checker.yaml`
- `normalization.yaml`
- `compare_config.yaml`
- `expected_rejections.yaml`

Shared implementation belongs under `src/sql_rewrite_bench/`:

- existing `local_result_checker.py` handles result comparison.
- future `sql_shape_validator.py` handles SQL static shape checks.
- future `plan_artifact_validator.py` handles plan/evidence artifact checks.
- future `engine_query_runner.py` may handle shared engine query execution.

Per-case copied implementations such as `run_engine_queries.py`, `check_results.py`, `check_sql_consistency.py`, `check_plan_artifacts.py`, and `run_checks.sh` are compatibility/template assets only, not clean v2 package contents.

## Validation Call Graph

Thin `validation/run_validation.sh` and `validation/run_plan_collection.sh` wrappers should resolve the case manifest, direct SQL paths, case-local schema profile, external schema refs, checker refs, and evidence refs, then call shared Python logic. New outputs must go to explicit local output roots, not case-local `runs/`.

## Folder-ordered Conversion Sequence

Future writable conversion must proceed in this order:

`manifest -> sql -> schema -> checker -> validation -> witness -> evidence -> metadata -> notes -> runs -> README/validator`

Each layer has a validation gate before proceeding. This prevents spreading mixed v1/v2 structures into more cases.

## Impact on Future Batch Conversion

The next writable pilot should update a small set of cases by layer. It should not convert one whole case manually and then repeat divergent decisions. The schema layer now requires `schema/schema_profile.yaml` plus external executable schema refs.

## Protected Boundary Summary

- Case files modified: no.
- Schemas modified: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Legacy repo modified: no.

## Exact Next Safe Action

Authorize a branch-only folder-ordered writable pilot that first normalizes manifest and SQL layers for the selected cases, then adds `schema/schema_profile.yaml` and external schema references before touching checker, validation, witness, evidence, metadata, notes, runs, README, or validator expectations.
