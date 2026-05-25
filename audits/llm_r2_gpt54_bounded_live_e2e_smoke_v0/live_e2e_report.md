# Live E2E Report

## Scope

The smoke selected six PostgreSQL Common-core rows: `PERF_0006`, `CONS_0036`, `PERF_0007`, `CONS_0005`, `CONS_0007`, and `LONGTAIL_0011`. No MySQL, Spark, Track A 120, verifier, official metrics, paper rendering, retained evidence promotion, or leaderboard generation was run.

## Generation And Extraction

- Live GPT-5.4 calls attempted: 6
- Candidates generated: 6
- Extraction status: all generated rows extracted exactly one SQL statement.
- Preflight status: all generated rows passed candidate preflight.

## DB, Checker, And Timing

- Source executable rows: 6
- Candidate executable rows: 5
- Checker exact rows: 5
- Timed rows: 5

## Failures

- `LONGTAIL_0011`: `candidate_execution_failed`; candidate captured from workspace candidate.sql; candidate preflight passed; parse status not checked; candidate SQL execution failed

`LONGTAIL_0011` generated a candidate and passed preflight, but candidate execution failed, so checker and timing were not eligible for that row.

## Boundary

This is adapted GPT-5.4 local diagnostic evidence only. It is not original LLM-R2 paper reproduction because the official LLM-R2 runtime, Java/rule-system execution, checkpoint inference, and demonstration selector were not used.

Next safe action: run a separately authorized PostgreSQL-only PG40 bounded diagnostic before any Track A 120 consideration.
