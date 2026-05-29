# case_package_v2_checker_validation_layers_pilot_v0

## Purpose and Scope

This branch-only writable pilot converted the next two folder-ordered v2 asset layers for five pilot cases:

- checker
- validation

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

The task did not convert witness, evidence, metadata, notes, runs, schema, or SQL layers. It did not run DB/checker execution, compute official metrics, render paper tables, update reports/results, change denominators, change case membership, or create leaderboard output.

## Cases Converted

All five pilot cases were converted or verified for the checker and validation layers.

Cases deferred: none.

## Checker Configuration Summary

Each pilot case has the clean v2 checker configuration file set:

- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`
- `checker/expected_rejections.yaml`

No per-case Python checker implementations were added. Stale checker references to nested SQL paths were aligned to direct v2 SQL paths where present, while legacy nested paths were retained as explicit compatibility metadata.

## Validation Wrapper Summary

Each pilot case now has the clean v2 validation entrypoints:

- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`

The wrappers are thin and fail closed. They parse/document future `--engine`, `--target`, and `--out` arguments; refuse case-local `runs/` as an output target; and do not run DB engines, checkers, official metrics, paper rendering, retained-evidence updates, or leaderboard output.

## Compatibility Scripts Retained

Existing engine-specific validation and plan-collection scripts were retained as compatibility assets:

- `validation/run_postgres_validation.sh`
- `validation/run_mysql_validation.sh`
- `validation/run_spark_validation.sh`
- `validation/run_postgres_plan_collection.sh`
- `validation/run_mysql_plan_collection.sh`
- `validation/run_spark_plan_collection.sh`

No old engine-specific validation scripts were deleted.

## Shared Checker/Validator Module Summary

The case-local checker layer remains configuration-only. Existing shared result comparison remains `src/sql_rewrite_bench/local_result_checker.py`. Future SQL static-shape checks and plan/evidence artifact checks remain planned shared modules and were not implemented in this task.

## Validation Summary

Static v2 validation passed for all five pilot cases. Unit tests under `tests/case_package_v2` passed. Remaining validator findings are expected witness/evidence layer warnings for the four non-PERF_0006 cases and are outside this task's layer scope.

## Protected Boundary Summary

- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Case-local runs deleted: no.
- Evidence deleted: no.
- Witness/metadata/notes/runs converted: no.
- Per-case Python checker implementations added: no.
- Legacy repo modified: no.

## Exact Next Safe Action

Authorize `case_package_v2_witness_evidence_layers_pilot_v0` to convert only witness and evidence references for the five pilot cases, still branch-only and without DB/checker execution, reports/results updates, denominator changes, paper-result changes, evidence deletion, case-local runs deletion, or leaderboard output.
