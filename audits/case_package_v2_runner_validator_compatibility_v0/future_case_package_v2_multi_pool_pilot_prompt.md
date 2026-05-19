# Future Prompt: case_package_v2_multi_pool_pilot_v0

Task title:

`case_package_v2_multi_pool_pilot_v0`

Branch:

`feature/case-package-v2-external-schema`

Purpose:

Run the next branch-only case package v2 pilot after `PERF_0006` reference validation. Pilot exactly:

- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Scope:

- Use the v2 resolver and validator added by `case_package_v2_runner_validator_compatibility_v0`.
- Convert only the listed cases.
- Use copy-first external schema/evidence references.
- Keep case-local `runs/` as legacy retained evidence.
- Do not merge to `main`.

Before conversion:

- Review `v2_compatibility_gaps.csv`.
- Decide whether to normalize `PERF_0006` manifest internal shape to canonical `schema_ref.engines`, `checker.config`, `evidence_ref`, and witness policy fields before expanding.

Hard boundaries:

- Do not modify `case_sets/`.
- Do not modify inventory.
- Do not modify reports/results.
- Do not change denominators.
- Do not change paper results.
- Do not run DB engines or checkers.
- Do not compute metrics.
- Do not render paper tables.
- Do not delete case-local schema or `runs/`.
- Do not create leaderboard output.

Validation:

- Run the v2 static validator on all pilot cases.
- Require all required paths to resolve safely.
- Record compatibility warnings rather than silently rewriting.
- Confirm no protected paths outside selected cases, repository specs, audits, and project-control files changed.

Expected outputs:

- multi-pool pilot audit summary
- per-case v2 reference checks
- per-case internal-format checks
- external schema/evidence mapping preview
- protected-boundary validation
- updated project-control run log and status
