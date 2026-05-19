# Validation Entrypoint Policy v1 Draft

Status: draft policy for case package v2 validation entrypoints

This policy defines the target validation script surface. It does not implement validators, run DB engines, run checkers, collect timing, write reports/results, or authorize case conversion.

## Target Entrypoints

Case packages should converge to:

```text
validation/run_validation.sh
validation/run_plan_collection.sh
```

These scripts are stable user/maintainer entrypoints. They should be thin wrappers around shared logic.

## Engine Argument Handling

Wrappers should accept an engine argument or environment variable after compatibility implementation, for example:

```bash
validation/run_validation.sh --engine postgres
validation/run_plan_collection.sh --engine postgres
```

Supported engines must be validated against the manifest and `schema_ref`.

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

## Shared Logic Location

Shared validation and plan-collection behavior should live in:

- `scripts/` for command-line wrappers
- `src/` for importable library code

Adding shared logic requires a separate implementation task.

## Compatibility With Old Engine-specific Scripts

Existing files such as `run_postgres_validation.sh` or `run_spark_plan_collection.sh` remain compatibility assets until wrappers are validated.

Compatibility scripts should not be deleted during v2 branch adoption unless a separate cleanup task proves that all callers use the new entrypoints.

## Manifest Resolution Requirements

Wrappers and validators must resolve:

- `sql.source`
- `sql.positives`
- `sql.negatives`
- `schema_ref`
- checker config paths
- `evidence_ref`

They must fail closed on missing required paths or unsupported engines.

## Output Policy

Validation wrappers must not write new output into case-local `runs/` by default.

Local validation or user-run output belongs under an approved output root such as `runs/user/<run_id>/` or a future explicitly authorized validation-output root.

## Boundaries

Validation entrypoints do not compute official metrics, render paper tables, update retained evidence, update reports/results, update denominators, change case-set membership, or create leaderboard output.
