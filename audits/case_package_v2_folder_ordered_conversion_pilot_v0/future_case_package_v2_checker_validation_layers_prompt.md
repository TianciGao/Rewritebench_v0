# Future Prompt: case_package_v2_checker_validation_layers_pilot_v0

This is a draft. Do not execute it as part of `case_package_v2_folder_ordered_conversion_pilot_v0`.

## Task

Convert only the checker and validation layers for the same five pilot cases after profile-first schema_ref validator compatibility is implemented.

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

## Scope

Allowed layers:

- `checker`
- `validation`

Do not modify witness, evidence, metadata, notes, runs, case_sets, inventory, reports, results, denominators, paper results, official metrics, DB/checker execution outputs, or leaderboard output.

## Required Work

- Keep `checker/` case-local configuration only.
- Normalize manifest checker references if needed.
- Add or normalize thin `validation/run_validation.sh` and `validation/run_plan_collection.sh` wrappers.
- Do not copy Python checker or engine execution logic into cases.
- Route future shared logic through `src/sql_rewrite_bench/local_result_checker.py` and planned shared modules.
- Preserve old engine-specific validation scripts as compatibility assets unless a separate cleanup task authorizes deletion.

## Stop Conditions

Stop on:

- profile-first schema_ref validator compatibility not implemented.
- wrapper would need to run DB/checker execution during conversion.
- wrapper writes to case-local runs/ by default.
- checker config missing or ambiguous.
- protected path changes.
- official metric computation or leaderboard output.

## Validation

Run static validation only unless explicitly authorized. No DB/checker execution should occur in this checker/validation layer pilot.
