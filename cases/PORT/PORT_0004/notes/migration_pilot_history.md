# Historical PORT_0004 Migration Pilot

This file preserves the legacy-compatible full-case pilot history before canonical-layout upgrade. Canonical completion is governed by the current `README.md`, `manifest.yaml`, `evidence/runs_retention.yaml`, and validator outputs.

# PORT_0004 Migration Pilot

This is the first copy-first full case migration pilot.

Scope:

- Applies only to `PORT_0004`.
- Not Common-core 40 migration.
- Not batch migration.
- Not authorization to delete the legacy `PORT_0004` case.

What happened:

- Source files were copied from the legacy repo into the release repo.
- Legacy source files remain unchanged.
- Legacy raw runs remain do-not-delete and mapped.
- No DB engines were run.
- No evidence was regenerated.

Claim boundaries:

- Denominator unchanged.
- Paper results unchanged.
- Common-core membership unchanged.
- No global leaderboard introduced.

Completion status:

- The initial copy-first attempt failed public hygiene on two copied Spark plan files.
- The release-repo copies were sanitized in place and canonical sanitized retained-plan copies were added under `evidence/retained_plans/`.
- Validator v0.2 full-case mode now passes for `PORT_0004`.
- This pilot is complete for `PORT_0004` only.
