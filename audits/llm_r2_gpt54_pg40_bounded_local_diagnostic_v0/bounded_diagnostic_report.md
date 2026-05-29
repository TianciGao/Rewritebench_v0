# Bounded Diagnostic Report

## Scope

This run selected the PostgreSQL Common-core v0 40 rows only. It is an adapted GPT-5.4 LLM-R2 local diagnostic route, not original LLM-R2 paper reproduction, not Track A 120, and not official metrics.

## Provider Status

- provider: `openai_compatible`
- model: `gpt-5.4`
- live gate: enabled
- raw responses saved: no
- official LLM-R2 runtime / `python src/LLM_R2.py` / Java rule-system / checkpoint / demo selector: not used

## Generation, Extraction, And Preflight

- selected: 40
- generated: 40
- preflight passed: 40
- all rows recorded `live_call=true`, `fake_runtime=false`, `rule_system_runtime_used=false`, `checkpoint_used=false`, and `demonstration_selector_used=false`.

## DB, Checker, And Timing

- source executable: 40
- candidate executable: 39
- exact: 39
- mismatch: 0
- timed exact rows: 34
- timing-ineligible rows:
- `PORT_0004`: `timing_scope_not_supported`
- `PORT_0013`: `timing_scope_not_supported`
- `PORT_0022`: `timing_scope_not_supported`
- `PORT_0024`: `timing_scope_not_supported`
- `PORT_0025`: `timing_scope_not_supported`
- `LONGTAIL_0011`: `candidate_execution_failed`

## Local Metrics Summary

- generation rate: 1.0
- execution coverage: 0.975
- result consistency: 0.975
- GM speedup: 1.009691483166132
- P10/P25/P50/P75/P90: 0.5650932995267253 / 0.91306615287767 / 0.9929224218407445 / 1.6245036973766611 / 1.7340646690442811

## Failure Frontier

- `LONGTAIL_0011`: `candidate_execution_failed`; candidate captured from workspace candidate.sql; candidate preflight passed; parse status not checked; candidate SQL execution failed

`LONGTAIL_0011` still fails candidate execution in this PG40 run after also failing in the 6-row smoke. It remains denominator-visible and was not replaced or dropped.

## Source-Like Behavior

- source-like/no-op diagnostic rows: 1
- source-like rows: CONS_0037

This classification is diagnostic only and is not POCR or a ranking metric.

## Readiness

The PG40 bounded diagnostic is stable enough for a route boundary/policy packet. It does not authorize Track A 120 because MySQL/Spark are unassessed and an engine-support/route-denominator policy would be required first.

Next safe action: write an LLM-R2 adapted PostgreSQL route boundary/policy packet and decide whether to stop at bounded PG evidence or authorize a separately scoped support assessment.
