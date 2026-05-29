# Bounded Diagnostic Report

This packet records a PostgreSQL-only Common-core 40 bounded local diagnostic for LearnedRewrite through the external HTTP runtime. It is not Track A 120 and not official metrics.

## Scope

- Case set: `common_core_v0`
- Engine: `postgres` only
- Selected rows: 40
- MySQL/Spark: not run
- Track A 120: not run

## Runtime

The external JAR was started from temp-only staging outside the release repo with `rules_for_selected/` staged under `/tmp`. The runtime was stopped after the diagnostic.

## Generation And Extraction

- Adapter-invoked rows: 40
- Candidate generated rows: 29
- Fail-closed/no-candidate rows: 11
- Runtime `status=false` rows: 11
- Extraction failures after successful runtime response: 0

## DB, Checker, Timing

- Source executable rows: 29
- Candidate executable rows: 23
- Exact rows: 17
- Mismatch rows: 6
- Candidate execution failed rows: 6
- Timed exact rows: 17

## local_metrics.py Summary

- Generation Rate: 0.725
- Execution Coverage Rate: 0.575
- Result Consistency Rate: 0.425
- GM Speedup: 1.0291029729677286
- P10/P25/P50/P75/P90: 0.8134186116858578 / 0.9784093859740545 / 1.0023559404279565 / 1.014471169398659 / 1.704766251233957

All values above are copied from local diagnostic run artifacts or local_metrics.py outputs; they are not official metrics or paper results.

## Failure Buckets

- `candidate_execution_failed`: 6
- `mismatch`: 6
- `no_candidate_sql`: 11
- `none`: 17

## Source-Like / No-Op Behavior

- Source-like generated candidates: 2
- Nontrivial generated candidates by string comparison: 27

This source-like review is diagnostic only and is not POCR.

## PERF_0006

`PERF_0006/postgres` was previously deferred because of TPC-H/date/comment-heavy shape. In this PG40 diagnostic it generated a candidate, executed successfully, checked exact, and timed successfully with speedup ratio `0.9657627294586701`.

## Readiness Verdict

LearnedRewrite is stable enough for a PostgreSQL route boundary/policy packet. It still needs explicit boundary decisions before any Track A support assessment because this PG40 result is single-engine only, has 11 fail-closed no-candidate rows, 6 candidate-execution failures, and no MySQL/Spark coverage.

Next safe action: write a LearnedRewrite PostgreSQL route boundary/policy packet and decide whether to stop at bounded PG appendix evidence or authorize a separate Track A support assessment.
