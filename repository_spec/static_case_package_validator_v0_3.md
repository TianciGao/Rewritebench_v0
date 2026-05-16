# Static Case Package Validator v0.3

Status: implemented

Validator path: `scripts/dev/validate_case_package.py`

## Purpose

Validator v0.3 adds a canonical-layout conformance gate after the completed `PORT_0008` canonical-layout full case migration pilot.

It is static only. It checks release-repo package structure, metadata consistency, evidence mapping, public hygiene, and claim boundaries. It does not migrate cases, run DB engines, execute validation scripts, regenerate plans, change denominators, change paper results, or change Common-core membership.

## Modes

- `evidence-pilot`: regression mode for completed sanitized evidence-mapping pilot slices.
- `full-case`: v0.2 mode for general full migrated case package completeness.
- `canonical-case`: v0.3 mode for canonical public-release layout conformance.

## Canonical-Case Checks

`canonical-case` mode checks:

- root `README.md`, `manifest.yaml`, and `evidence/runs_retention.yaml`;
- canonical SQL layout under `sql/`;
- canonical schema layout under `schema/<engine>/`;
- data profiles under `data/`;
- checker configuration under `checker/`;
- validation assets under `validation/`, including a legacy-output caveat when scripts write to case-local `runs/`;
- retained evidence under `evidence/retained_controls/`, `evidence/retained_plans/`, and `evidence/hard_negative/`;
- package validation summary JSON;
- metadata YAML under `metadata/`;
- migration notes under `notes/`;
- no raw `runs/` wholesale publication;
- manifest paths point into canonical directories;
- runs-retention semantics preserve original legacy mappings and do-not-delete status;
- sanitized public copies are public-safe;
- public hygiene scan passes;
- claim boundaries do not imply denominator, paper-result, membership, or benchmark-scope changes.

The mode accepts `validation/run_pg_validation.sh` as a transitional alias for PostgreSQL validation because the completed `PORT_0008` canonical pilot currently uses that file name. It emits a warning for that alias.

## What It Does Not Check

`canonical-case` mode does not certify scientific correctness, SQL equivalence, runtime behavior, timing, plan semantics, or DB reproducibility. It does not inspect or mutate the legacy repository.

## Examples

Strict canonical validation:

```bash
python scripts/dev/validate_case_package.py \
  --mode canonical-case \
  --case cases/PORT/PORT_0008
```

Advisory validation against a legacy-compatible pilot:

```bash
python scripts/dev/validate_case_package.py \
  --mode canonical-case \
  --allow-failures \
  --case cases/PORT/PORT_0004
```

## Expected Results

- `PORT_0008` should pass `canonical-case` mode because it is the first canonical-layout full-case pilot.
- `PORT_0004` should fail `canonical-case` mode in advisory usage because it is a completed legacy-compatible full-case pilot, not the canonical-layout template.
- `PORT_0004` and `PORT_0008` should both continue to pass `full-case` mode.
- The six blocked-PORT evidence slices should continue to pass `evidence-pilot` mode.

## Migration Boundary

Passing `canonical-case` does not start Common-core 40 migration and does not change denominators, paper results, case membership, or case admission. It only says the checked release-repo case package conforms to the static canonical-layout gate.
