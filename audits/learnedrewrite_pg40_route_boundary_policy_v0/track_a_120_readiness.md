# Track A 120 Readiness

`ready_for_track_a_120: no`

LearnedRewrite is not ready for Track A 120.

Blockers:

- PG40 exact/result-consistent rows are only 17/40.
- Generated candidates are only 29/40.
- Candidate executable rows are only 23/40.
- Fail-closed/no-candidate rows are 11/40.
- Candidate execution failures are 6/40.
- MySQL is unsupported/not assessed.
- Spark is unsupported/not assessed.
- Runtime/schema/request failure frontier needs triage before a broader route.
- Generated SQL execution failure frontier needs triage before a broader route.

Required policy before any broader run:

- Engine support policy: define whether LearnedRewrite is PostgreSQL-only or whether MySQL/Spark wrappers are explicitly supported.
- Unsupported row policy: define how runtime `status=false`, unsupported engines, schema serialization failures, and no-candidate rows remain denominator-visible.
- Route denominator policy: define whether any future route is bounded PG-only, appendix-only, or Track A same-engine 120.
- Failure bucket policy: define stable buckets for runtime/schema failure, extraction failure, candidate execution failure, checker mismatch, and exact rows.

Until those policies exist, LearnedRewrite should remain bounded PostgreSQL appendix diagnostic evidence only.
