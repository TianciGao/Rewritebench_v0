# Timing Readiness Review

## Recommendation

Do not start U8 as an implementation task now. If the maintainer wants to continue user-entry timing work, authorize U8 as design-only after explicitly approving a timing protocol scope. Otherwise pause user-entry work after U0-U7 and return to release-surface metadata.

## Exact + Timed Requirement

Performance interpretation is valid only for rows that are both locally exact and timed under an approved timing protocol. Current user-entry outputs can record local exactness for optional PostgreSQL/checker diagnostics, but timing collection and exact + timed eligibility are not implemented.

## Warmup / Repetition / Timeout / Cache Policy

No approved policy currently defines:

- warmup count
- repetition count
- timeout handling
- cache state
- randomized or fixed execution order
- source/candidate interleaving
- machine/environment disclosure

U8 must not implement timing before these policy choices are designed and approved.

## Raw Timing Sample Ownership

Future raw timing samples should be owned by engine execution modules, not by `user_run.py`, `user_quality_report.py`, or `tag_slices.py`. Raw timing samples must remain local diagnostics until a separate official metrics authorization exists.

## Engine Version Capture

Any timing design must capture engine version and relevant environment details. PostgreSQL version capture should be designed first; MySQL/Spark remain fail-closed and should not imply timing support.

## Official Metrics Boundary

Official timing metrics remain unauthorized. User-entry timing diagnostics, if later implemented, must not compute GM_Speedup, Speedup Ratio Percentiles, SpeedupTransferRate, paper tables, report rows, or leaderboard entries.

## SpeedupTransferRate

SpeedupTransferRate remains deferred. It requires paired source-engine and target-engine timing semantics that are outside the current U0-U7 local diagnostic harness.
