# Common-core 40 Next Batch Recommendation

This recommendation does not execute migration.

## Primary Recommendation

Migrate a small PERF sanitized-plan batch after human review of this audit:

- `PERF_0007`
- `PERF_0008`
- `PERF_0013`

Why these cases:

- They are closest to the completed `PERF_0006` canonical-layout pilot.
- They exercise the same performance-boundary discipline without creating new timing or speedup claims.
- They appear suitable for a repeatable sanitized Spark plan workflow.
- Batch size 3 is large enough to test wave mechanics but small enough to stop safely.

## Fallback Recommendation

Migrate only `PERF_0007` as a one-case follow-up if the maintainer wants the lowest-risk post-pilot step.

## Why Not Other Cases Yet

- CONS cases need expected rejection approvals.
- LONGTAIL cases need structural/hard-negative boundary review.
- PORT cases need dialect and sanitized-plan handling; `PORT_0022`, `PORT_0024`, and `PORT_0025` remain manual-review/defer.
- Migrating all remaining 35 cases at once would combine incompatible risk classes.

## Expected Codex Autonomy

Medium autonomy for the primary PERF batch after prompt approval. The user does not need to supervise every file operation, but should be available for abort-condition decisions.

## Stop Conditions

- Dirty release repo at start.
- Missing legacy files.
- Public hygiene failure after sanitization.
- Raw Spark local path appears in public retained evidence.
- File hash mismatch for copied public-safe files.
- Manifest and runs-retention contradiction.
- Validator v0.3 full-case or canonical-case failure.
- Any denominator, paper-result, case-membership, or raw-legacy-evidence change.
- Any new speedup, timing, ranking, or leaderboard claim.
- `git add .` or broad commit scope attempted.

## Future Prompt Outline

A future prompt should explicitly list the selected PERF cases, use copy-first canonical migration, create per-case audits and `runs_retention.yaml`, sanitize Spark plans only in the release repo, run validator v0.3 full-case and canonical-case for each migrated case, run regressions against existing pilots, update project controls, and commit explicit paths only.
