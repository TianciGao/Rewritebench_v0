# Validation Entrypoint Policy v1 Draft

Status: draft policy for case package v2 validation entrypoints

This policy defines the target validation script surface. It does not implement validators, run DB engines, run checkers, collect timing, write reports/results, or authorize case conversion.

## Target Entrypoints

Case packages should converge to:

```text
validation/run_validation.sh
validation/run_plan_collection.sh
validation/run_engine_queries.py
```

These files are stable user/maintainer entrypoints. The shell scripts are thin wrappers. The Python entrypoint is a short case-local shim that delegates to shared logic under `src/sql_rewrite_bench/validation/`.

## Engine Argument Handling

Wrappers should accept an engine argument or environment variable after compatibility implementation, for example:

```bash
validation/run_validation.sh --engine postgres
validation/run_plan_collection.sh --engine postgres
```

Supported engines must be validated against the manifest and `schema.external_profile`.

## Target Argument Handling

Wrappers may support target selection such as:

- source control
- positive control
- hard-negative control
- candidate SQL path

Target semantics must be explicit and must not imply official metrics or leaderboard ranking.

## Thin-wrapper Principle

Case-local scripts should:

- find the repository root
- locate and parse `manifest.yaml`
- dispatch to shared logic in `scripts/` or `src/`
- pass engine and target arguments
- write local outputs only to approved local output roots

Case-local scripts should not contain large duplicated runner logic.

`validation/run_engine_queries.py` is required only as a thin shim. It must not contain engine-specific execution implementation, hardcoded case IDs, credentials, case-local `runs/` writes, metrics/reporting behavior, or leaderboard creation.

Case packages should avoid duplicated per-case implementations of:

- `check_results.py`
- `check_sql_consistency.py`
- `check_plan_artifacts.py`
- `run_checks.sh`

Those names may exist only as compatibility assets or templates until shared modules replace them. `run_engine_queries.py` is the exception: it is required as a thin local entrypoint that imports and delegates to shared code.

## Shared Logic Location

Shared validation and plan-collection behavior should live in:

- `src/sql_rewrite_bench/validation/engine_query_runner.py`
- `src/sql_rewrite_bench/validation/plan_collection_runner.py`
- equivalent shared modules under `src/sql_rewrite_bench/validation/`

Initial shared modules may fail closed until DB execution is separately authorized.

## Shared Module Call Graph

Clean v2 validation wrappers should follow this shared call graph:

1. User or maintainer invokes `validation/run_validation.sh` or `validation/run_plan_collection.sh`.
2. Wrapper resolves the repository root and calls `validation/run_engine_queries.py`.
3. The shim resolves the case directory and delegates to `src/sql_rewrite_bench/validation/engine_query_runner.py` or `plan_collection_runner.py`.
4. Manifest resolution loads direct SQL paths, `schema.external_profile`, case-local `schema/schema_profile.yaml`, checker config paths, witness policy, and `evidence_policy`.
5. Engine query execution, when authorized by a separate task, dispatches to shared engine-runner logic.
6. Result comparison dispatches to existing `src/sql_rewrite_bench/local_result_checker.py`.
7. SQL static shape checks dispatch to future `src/sql_rewrite_bench/sql_shape_validator.py`.
8. Plan and evidence artifact checks dispatch to future `src/sql_rewrite_bench/plan_artifact_validator.py`.
9. Outputs are written only to approved local output roots, never to case-local `runs/` by default.

`local_result_checker.py` exists today as the shared local result comparison implementation. DB execution remains unauthorized until a separate task implements and approves it.

## Compatibility With Old Engine-specific Scripts

Existing files such as `run_postgres_validation.sh` or `run_spark_plan_collection.sh` remain compatibility assets until wrappers are validated.

Compatibility scripts should not be deleted during v2 branch adoption unless a separate cleanup task proves that all callers use the new entrypoints.

## Manifest Resolution Requirements

Wrappers and validators must resolve:

- `sql.source`
- `sql.positive_rewrites`
- `sql.hard_negatives`
- `schema.external_profile`
- `schema/schema_profile.yaml`
- checker config paths
- validation/run_engine_queries.py thin shim
- witness policy
- `evidence_policy`

They must fail closed on missing required paths or unsupported engines.

## Output Policy

Validation wrappers must not write new output into case-local `runs/` by default.

Local validation or user-run output belongs under an approved output root such as `runs/user/<run_id>/` or a future explicitly authorized validation-output root.

## Boundaries

Validation entrypoints do not compute official metrics, render paper tables, update retained evidence, update reports/results, update denominators, change case-set membership, or create leaderboard output.
