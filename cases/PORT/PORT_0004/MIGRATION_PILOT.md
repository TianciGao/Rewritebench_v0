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

- Full case migration status for this case is pilot-complete only after validator v0.2 passes.
- If validator v0.2 or public hygiene checks fail, this remains a failed copy-first pilot attempt requiring release-repo-only remediation or an approved evidence mapping decision.
