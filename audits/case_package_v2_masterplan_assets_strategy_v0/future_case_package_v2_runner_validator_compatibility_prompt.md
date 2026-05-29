# Future Prompt: case_package_v2_runner_validator_compatibility_v0

Task title:

`case_package_v2_runner_validator_compatibility_v0`

Purpose:

Implement non-destructive compatibility checks for case package v2 manifest references on `feature/case-package-v2-external-schema`.

Scope:

- Resolve `schema_ref` for `PERF_0006`.
- Define and validate `evidence_ref` shape without moving evidence.
- Validate direct v2 SQL paths.
- Preserve v1 fallback path support during the branch pilot.
- Recheck `PERF_0006` only.

Hard boundaries:

- Do not bulk-convert cases.
- Do not modify any case except if the task explicitly authorizes a minimal `PERF_0006` manifest compatibility correction.
- Do not modify `case_sets/`, inventory, reports, results, denominators, paper results, retained evidence, or raw legacy evidence.
- Do not run DB engines or checkers unless separately authorized.
- Do not compute official metrics, render paper tables, update retained evidence, or create a leaderboard.
- Do not merge to main.

Expected implementation areas:

- static manifest resolver for `schema_ref`
- static manifest resolver for `evidence_ref`
- v2 manifest path validation
- tests or smoke checks that prove v1 compatibility paths still work
- audit outputs documenting compatibility status and remaining gaps

Validation:

- branch check for `feature/case-package-v2-external-schema`
- static path validation for `PERF_0006`
- no protected path changes
- `git diff --check`
- no case-local `runs/` writes

Next step after success:

Authorize a branch-only multi-pool v2 pilot for `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
