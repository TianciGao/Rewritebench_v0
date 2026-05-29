# Future Prompt: case_package_v2_folder_ordered_conversion_pilot_v0

This prompt is a draft. Do not execute it as part of `case_package_v2_rulebook_refinement_folder_order_v0`.

## Task

Run a branch-only writable v2 conversion pilot by folder layer, not by arbitrary per-case edits.

Repository:

- Work only on `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repository.

Pilot scope:

- Use the selected pilot cases from the latest read-only batch converter plan.
- Convert only cases whose stop conditions have been resolved.
- Do not touch `case_sets/`, inventory, reports, results, denominators, paper results, retained evidence outputs, or leaderboard outputs.

## Required Order

Proceed by layer:

1. `manifest`
2. `sql`
3. `schema`
4. `checker`
5. `validation`
6. `witness`
7. `evidence`
8. `metadata`
9. `notes`
10. `runs`
11. `README/validator`

Do not complete all edits for one case while leaving other selected cases in mixed states. Keep each layer coherent across the selected pilot set before moving to the next layer.

## Schema Rule

Clean v2 keeps case-local `schema/` only for `schema/schema_profile.yaml`.

Executable DDL/load must be external:

```text
schemas/<SCHEMA_ID>/<engine>/ddl.sql
schemas/<SCHEMA_ID>/<engine>/load.sql
```

Do not delete case-local per-engine schema compatibility files unless the prompt explicitly authorizes cleanup and retention/compatibility validation passes.

## Checker and Validation Rule

Case-local `checker/` stores config only.

Case-local `validation/` stores only thin wrappers:

- `validation/run_validation.sh`
- `validation/run_plan_collection.sh`

Shared implementation must live in `src/sql_rewrite_bench/` or shared scripts. Do not copy checker or engine execution Python logic into each case.

## Stop Conditions

Stop on:

- unresolved schema id or external schema target
- missing source SQL or positive/negative SQL mapping
- missing checker configuration
- uncertain retained evidence classification
- non-empty case-local runs without retention mapping
- absolute local paths or sensitive traces
- protected path changes
- denominator or paper result changes
- official metric computation
- DB/checker execution unless explicitly authorized
- leaderboard output

## Validation

Run static v2 validation only unless a separate prompt authorizes execution. Confirm no protected paths changed and no case-local `runs/` outputs were created.
