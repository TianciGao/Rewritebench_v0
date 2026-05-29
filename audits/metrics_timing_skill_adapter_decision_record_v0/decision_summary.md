# Decision Summary

Decision number: `D032`

Title: `Latest paper metrics/timing phase and external skill-adapter deferral`

## Decision Recorded

- Proceed next with metrics/timing protocol alignment and performance-layer planning after the user-entry local diagnostic layer.
- Treat latest paper Table 6 as the current target for metric naming and formula alignment.
- Preserve exact-gated and timed-gated performance interpretation.
- Require paired source/candidate timing artifacts in the same engine/environment/run context before performance metrics can be computed.
- Keep Regression@20 as a reporting diagnostic / open question unless separately confirmed as a formal latest-paper metric.
- Defer Positive Operation Coverage Rate until the collaborator's operation-atom script and schema are stable.
- Do not create or populate `skill/` folders yet.
- Do not infer operation atoms from taxonomy tags, SQL text, or `positive.sql`.

## Relationship To Existing Decisions

D018 remains historical context for the older formalized Metrics Contract v1. D032 records the latest-paper alignment direction and requires a follow-up metrics contract delta/audit before implementation.

## Non-Authorization

D032 does not authorize timing implementation, metrics computation, POCR implementation, skill folder creation, operation atom inference, reports/results updates, retained-evidence promotion, paper table rendering, leaderboard output, denominator changes, case membership changes, paper result changes, or case package layout changes.
