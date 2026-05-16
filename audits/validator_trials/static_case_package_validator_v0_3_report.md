# Static Case Package Validator v0.3 Report

Date: 2026-05-16

## Scope

This report records the validator v0.3 upgrade adding `canonical-case` mode. No case migration, DB validation, evidence regeneration, denominator change, paper-result change, case membership change, or legacy mutation occurred.

## What Changed From v0.2

- Added `--mode canonical-case`.
- Preserved existing `evidence-pilot` and `full-case` modes.
- Added canonical layout checks for root files, `sql/`, `schema/`, `data/`, `checker/`, `validation/`, `evidence/`, `metadata/`, `notes/`, and `runs/` policy.
- Added canonical manifest and runs-retention semantic checks.
- Added stricter public hygiene and claim-boundary checks for canonical packages.
- Added dedicated canonical-case CSV output fields.

## Trial Results

Trial 1, evidence-pilot regression:

- Result: PASS 6/6.
- Cases: `PORT_0008`, `PORT_0012`, `PORT_0013`, `PORT_0022`, `PORT_0025`, `PORT_0024`.

Trial 2, full-case regression:

- Result: PASS 2/2.
- Cases: `PORT_0004`, `PORT_0008`.

Trial 3, canonical-case strict validation:

- Result: PASS 1/1.
- Case: `PORT_0008`.
- Note: `PORT_0008` passes with a warning that `validation/run_pg_validation.sh` is accepted as a transitional PostgreSQL validation alias.

Trial 4, canonical-case advisory validation:

- Result: expected advisory failure.
- Case: `PORT_0004`.
- Reason: `PORT_0004` is a legacy-compatible full-case pilot and intentionally does not satisfy the canonical layout.

## Interpretation

`PORT_0008` is validated as the first canonical-layout full-case pilot. `PORT_0004` remains a completed legacy-compatible full-case pilot and should not be treated as the canonical template.

## Next Safe Action

Review validator v0.3 results, then decide whether to extend canonical layout checks further, plan the next single-case pilot, or continue case-universe/report/script audits. Do not start Common-core 40 migration.
