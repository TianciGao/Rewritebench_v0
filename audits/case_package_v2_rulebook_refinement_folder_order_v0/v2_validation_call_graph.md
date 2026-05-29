# Case Package v2 Validation Call Graph

This is a design record only. It does not create new validator modules or run DB/checker execution.

## User-facing Commands

Clean v2 exposes two case-local entrypoints:

```bash
cases/<POOL>/<CASE_ID>/validation/run_validation.sh --engine postgres --target all
cases/<POOL>/<CASE_ID>/validation/run_plan_collection.sh --engine postgres --target all
```

The wrappers are thin. They find the repository root, locate `manifest.yaml`, pass arguments, and call shared logic.

## Manifest Resolution

Shared logic resolves:

- `sql.source`
- `sql.positives`
- `sql.negatives`
- `schema_ref.schema_id`
- `schema_ref.profile`
- `schema_ref.case_profile` or `schema/schema_profile.yaml`
- `schema_ref.engines.<engine>.ddl`
- `schema_ref.engines.<engine>.load`
- `checker.config`
- `checker.normalization`
- `checker.compare_config`
- `checker.expected_rejections`
- `evidence_ref`

All paths must be repository-relative or case-relative according to the v2 contract. Absolute local paths fail validation.

## Schema Profile Resolution

`schema/schema_profile.yaml` is the case-facing schema summary. It links to `schemas/<SCHEMA_ID>/schema_profile.yaml`, which links to executable DDL/load.

Executable DB setup reads from external `schemas/<SCHEMA_ID>/<engine>/ddl.sql` and `load.sql` only after a separate execution task authorizes it.

## Engine Runner

Future `src/sql_rewrite_bench/engine_query_runner.py` may own shared engine query execution. Case packages must not copy engine query execution implementation per case.

Any engine runner must write outputs only to approved local output roots and must never write new output into case-local `runs/` by default.

## Local Result Checker

Existing `src/sql_rewrite_bench/local_result_checker.py` owns local source-result versus candidate-result comparison for user-run diagnostics.

It is local diagnostic support only. It does not compute official metrics, update retained evidence, render paper tables, or create leaderboard output.

## Future SQL Shape Validator

Future `src/sql_rewrite_bench/sql_shape_validator.py` should own static SQL shape checks, including direct v2 SQL path validation and any source/positive/negative consistency checks.

This module is not created by this task.

## Future Plan Artifact Validator

Future `src/sql_rewrite_bench/plan_artifact_validator.py` should own plan and evidence artifact checks referenced through `evidence_ref`.

This module is not created by this task.

## Output Policy

Validation wrappers and shared modules must write new outputs only to explicit local output roots. They must not write new outputs to:

- case-local `runs/`
- `results/`
- `reports/`
- `schemas/`
- `case_sets/`
- inventory files

They must not compute official metrics, render paper tables, update retained evidence, change denominators, change paper results, or create global leaderboard output.
