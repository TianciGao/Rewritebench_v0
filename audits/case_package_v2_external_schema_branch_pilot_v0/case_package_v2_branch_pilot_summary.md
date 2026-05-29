# Case Package v2 External-schema Branch Pilot v0

## Purpose and Scope

This branch pilot starts controlled adoption of the case package v2 direction with external reusable schema packages. It is branch-only and pilot-only.

Branch:

`feature/case-package-v2-external-schema`

Pilot case:

`PERF_0006`

This task did not perform a main-branch bulk migration, full Common-core conversion, denominator update, `case_sets/` update, reports/results migration, paper-result update, official metric computation, paper table rendering, global leaderboard creation, retained-evidence deletion, raw legacy evidence modification, DB execution, checker execution, timing collection, or LLM calls.

## Major Decision Summary

Decision `D019` was added to `project_control/DECISION_LOG.md`.

The decision freezes further B-line user-entry and DB/checker expansion while the v2 external-schema package standard is piloted on:

`feature/case-package-v2-external-schema`

The decision adopts:

- direct SQL paths under `sql/`
- `witness/` for data profile and correct-result material
- `checker/` for comparison and expected-rejection rules
- `validation/` for reproducible entrypoints
- case-local `runs/` as legacy retained evidence only
- external reusable `schemas/<SCHEMA_ID>/` packages
- manifest `schema_ref` references

No denominator, case-set, paper result, retained evidence, reports/results, official metric, paper table, raw legacy evidence, or leaderboard change is authorized by the decision.

## B-line Freeze Statement

Further B-line user-entry/DB-checker expansion is frozen until the case package v2 external-schema pilot is reviewed. The existing user-entry and DB/checker MVPs remain reference context, but broad execution expansion should wait until v2 path and schema-ref compatibility are settled.

## v2 Template Summary

Target pilot layout:

```text
cases/<POOL>/<CASE_ID>/
  README.md
  manifest.yaml
  sql/source.sql
  sql/pos_01.sql
  sql/neg_01.sql
  witness/data_profile.yaml
  witness/correct_result.csv
  checker/
  validation/run_validation.sh
  validation/run_plan_collection.sh
  runs/  # legacy retained evidence only
```

External schema layout:

```text
schemas/tpch_common_core_v0/
  schema_profile.yaml
  postgres/ddl.sql
  postgres/load.sql
  mysql/ddl.sql
  mysql/load.sql
  spark/ddl.sql
  spark/load.sql
```

## External Schema Policy

This pilot is copy-first. Schema files were copied out to `schemas/tpch_common_core_v0/`, and `PERF_0006` now has manifest `schema_ref` entries for postgres, mysql, and spark.

The old case-local `schema/` directory was not deleted. `schema/schema_profile.yaml` now marks the case-local schema as a retained compatibility copy for the branch pilot.

## PERF_0006 Pilot Conversion Summary

Converted or added:

- `sql/pos_01.sql`
- `sql/neg_01.sql`
- `witness/data_profile.yaml`
- `witness/correct_result.csv`
- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`
- `schemas/tpch_common_core_v0/schema_profile.yaml`
- `schemas/tpch_common_core_v0/postgres/ddl.sql`
- `schemas/tpch_common_core_v0/postgres/load.sql`
- `schemas/tpch_common_core_v0/mysql/ddl.sql`
- `schemas/tpch_common_core_v0/mysql/load.sql`
- `schemas/tpch_common_core_v0/spark/ddl.sql`
- `schemas/tpch_common_core_v0/spark/load.sql`

Updated:

- `README.md`
- `manifest.yaml`
- `checker/checker.yaml`
- `checker/expected_rejections.yaml`
- `schema/schema_profile.yaml`

Retained for compatibility:

- `sql/positives/pos_01.sql`
- `sql/negatives/neg_01.sql`
- `schema/`
- `runs/`

## Files Moved, Copied, or Created

No destructive moves were performed. The pilot used copy-first changes:

- positive and negative SQL were copied to direct v2 paths
- schema DDL/load files were copied to `schemas/tpch_common_core_v0/`
- witness files and validation wrappers were created
- old case-local schema and runs directories were preserved

## Compatibility Risks

- Current DB/checker runner code still resolves case-local `schema/postgres/ddl.sql` and `schema/postgres/load.sql`; it has not been updated to consume manifest `schema_ref`.
- Existing engine-specific validation scripts still reference old nested SQL and case-local schema paths and may write to case-local `runs/` if executed. The new v2 wrapper scripts intentionally do not run DB engines in this branch pilot.
- Optional user-entry CI smoke passed help/tests/dry-run/dummy-adapter steps but failed its protected-path guard because this branch intentionally modifies `cases/PERF/PERF_0006`.

No runner/source-code patch was made in this pilot.

## Validation Summary

Static validation passed:

- branch is `feature/case-package-v2-external-schema`
- only `PERF_0006` case package was modified
- `schemas/tpch_common_core_v0/` exists
- manifest parses
- schema profile parses
- `schema_ref` exists
- direct source/positive/negative SQL paths exist
- witness directory exists
- checker config paths still exist
- case-local `runs/` retained
- `case_sets/`, inventory, reports/results, denominators, paper results, and raw legacy evidence unchanged
- no official metrics, paper tables, or leaderboard created
- `git diff --check` passed

## Protected Boundary Summary

Unchanged:

- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- denominator files
- paper result files
- raw legacy evidence
- legacy repository

No case-local `runs/` deletion occurred.

## Exact Next Safe Action

Review the `PERF_0006` v2 external-schema branch pilot. If accepted, authorize a branch-only expansion to `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011` without merging to `main` until v2 validators and runner `schema_ref` compatibility are explicitly approved.
