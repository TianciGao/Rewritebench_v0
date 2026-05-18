# Wave 004 Policy Or Manual Questions

Wave 004 cannot proceed as a migration wave using only current wave 002/003 policies because no remaining rows are auto or policy-approved candidates.

## Questions To Resolve Before Migration

1. Can missing-checker backlog cases be standardized as package shells if clearly marked `checker_missing` and excluded from paper/report/denominator claims, or is checker presence required for any public package?
2. For manual-review cases with otherwise complete core assets, what exact hard-negative/checker approval evidence is sufficient to move them into a policy-approved migration bucket?
3. Should orphan/unregistered cases be reconciled into governance previews before package standardization, or should they remain excluded until inventory/registry alignment is separately authorized?
4. Can cases with missing schema but complete SQL/checker assets be standardized with `schema_not_retained`, or should they remain manual-review/backlog?
5. Should wave 004 be a blocker-resolution packet only, with migration deferred until a nonzero auto/policy-approved queue exists?

## Current Recommendation

Run a blocker-resolution task first. Do not execute wave 004 package migration until the selection CSV contains nonzero `wave_004_auto_migration_candidate` or `wave_004_policy_approved_candidate` rows.
