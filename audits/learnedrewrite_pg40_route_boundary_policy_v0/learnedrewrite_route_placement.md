# LearnedRewrite Route Placement

Recommended public v0 placement: bounded PostgreSQL prior-method evidence / appendix diagnostic.

LearnedRewrite should not be promoted to tri-engine Track A 120 for public v0 based on the current evidence.

Rationale:

- The only real-runtime Common-core diagnostic is PostgreSQL-only.
- PG40 exact/result-consistent coverage is 17/40.
- PG40 generation coverage is 29/40.
- PG40 execution coverage is 23/40.
- The failure frontier remains substantial: 11 fail-closed/no-candidate rows, 6 candidate execution failures, and 6 mismatches.
- MySQL and Spark were not run, not assessed, and are not currently covered by a LearnedRewrite engine-support policy.
- LearnedRewrite uses an external Java/Calcite runtime with schema/request-shape sensitivity, so unsupported rows must remain visible rather than silently dropped.

Policy:

- Report LearnedRewrite only as bounded PostgreSQL local diagnostic appendix evidence unless a later task explicitly authorizes more.
- Do not merge LearnedRewrite into the main Track A same-engine leaderboard-style narrative. The repository has no global leaderboard.
- Do not compare LearnedRewrite as a tri-engine peer to methods that have a 120-row Track A denominator.
- Do not claim original-paper reproduction. This is an adapted local diagnostic wrapper over the recovered external runtime.
- Do not treat runtime/schema limitations as method success or as hidden exclusions.

Broader route work requires a separate authorization covering engine support, unsupported-row handling, denominator scope, and failure-bucket interpretation.
