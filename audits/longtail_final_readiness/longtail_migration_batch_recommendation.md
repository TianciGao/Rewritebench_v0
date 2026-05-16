# LONGTAIL Migration Batch Recommendation

Date: 2026-05-16

## Primary Batch

Selected cases: `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024`.

Recommendation: migrate all five in one bounded final LONGTAIL canonical migration batch after maintainer approval of expected rejection wording. The cases share the `LONGTAIL_0011` canonical package pattern, retained tri-engine evidence shape, Spark plan sanitization requirement, validation-script caveat, and no-workload-frequency boundary.

## Fallback Batch

Selected cases: `LONGTAIL_0012`, `LONGTAIL_0013`.

Use the fallback if the maintainer wants the lower-risk path or if the Stack-substrate trio needs additional provenance wording. After this pair passes, migrate `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` as a second bounded batch.

## Whether To Split

All five can be migrated together only after approval because this planning wave found clear hard-negative explanations and no defer-only cases. Split the wave if any approval wording is disputed, if Spark plan sanitization produces a public hygiene failure, or if validation script adaptation reveals a systemic issue.

## Expected Codex Autonomy

Medium after approval. Codex can execute the bounded migration from static evidence, but the user should be reachable for abort-condition decisions because the prior readiness audit marked LONGTAIL as low-autonomy before this review.

## User Presence

User approval is required before migration. During migration, user presence is not required for every file operation, but the user should be available if a case fails validation or a boundary question appears.

## Stop Conditions

- Dirty release repo at start.
- Missing legacy SQL, schema, witness, result evidence, or plan evidence.
- Any public hygiene failure after Spark plan sanitization.
- Any raw `file:/tmp`, `/tmp/`, local path, WSL-local wording, prompt/token/API trace, or raw log path remains in public retained evidence.
- Any validator v0.3 full-case or canonical-case failure.
- Any denominator, paper-result, case-membership, `case_sets/`, reports/results, or raw legacy evidence change.
- Any workload-frequency, production-frequency, timing, speedup, leaderboard, or new benchmark result claim.
- Any attempt to use `git add .`.

Do not start blind Common-core 40 migration.
