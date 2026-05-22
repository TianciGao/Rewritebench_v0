# Metrics Timing Skill Adapter Decision Record

Verdict: `completed`

This audit records durable decision `D032: Latest paper metrics/timing phase and external skill-adapter deferral` in `project_control/DECISION_LOG.md`.

The decision records that the next project line should move from completed user-entry local diagnostics toward metrics/timing protocol alignment and performance-layer planning, while keeping implementation of timing, metrics computation, POCR, skill folders, reports/results, retained evidence, paper rendering, and leaderboard output deferred.

## Context

The user-entry/local diagnostic layer is complete enough for the next planning phase:

- adapter entry
- candidate capture
- candidate preflight
- PostgreSQL/MySQL/Spark local execution
- `local_result_checker`
- failure buckets
- quality summary
- tag slices
- label-only mismatch diagnostics
- strict-label policy documentation

The latest paper Table 6 scope supplied for this decision differs from the older repository Metrics Contract v1. The older contract included Attribution Coverage and Speedup Retention; the latest target uses Positive Operation Coverage Rate and Cross-Engine GM Speedup Ratio.

No local copy of `Beyond_Faster_SQL (5).pdf` was found under `/home/tianci_gao` during this task, so the decision records the latest-paper scope from the task context rather than extracting it from a local PDF.

## Boundary

This is decision-recording and audit-only. It does not implement timing, metrics computation, POCR, skill folders, case-package changes, reports/results migration, retained-evidence promotion, paper rendering, or leaderboard output.

## Next Safe Action

Run a latest-paper metrics/timing protocol alignment audit that compares D032/Table 6 against the existing `repository_spec/metrics_contract_v1.md` before any timing schema or metrics implementation work.
