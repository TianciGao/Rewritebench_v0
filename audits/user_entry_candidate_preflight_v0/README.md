# User-Entry Candidate Preflight v0

## Purpose

This packet records U3 candidate preflight v0 for the local user-entry diagnostic path.

Candidate preflight runs after adapter candidate capture and before optional PostgreSQL DB/checker diagnostics. It is a conservative text-level readiness and safety gate for generated candidate SQL. It is not semantic equivalence checking, DB execution, checker execution, timing, official metrics, paper table rendering, retained-evidence parsing, reports/results updating, or leaderboard creation.

## Implementation Summary

- Added `src/sql_rewrite_bench/candidate_preflight.py`.
- Integrated preflight into `src/sql_rewrite_bench/user_run.py` after adapter capture.
- Added local ledger fields for candidate preflight status, pass flag, failure class, safety status, parse status, and source-like status.
- Added failure bucket `candidate_preflight_failed` for generated candidates that fail preflight.
- Added tests for valid query candidates, empty candidates, unsafe statements, multi-statement candidates, unsupported top-level statements, source-like diagnostics, and DB/checker fail-closed behavior with a mocked executor.

## Verdict

U3 candidate preflight v0 is complete for local diagnostics.

## Boundary

- Quality report implemented: no.
- Tag slicing implemented: no.
- Timing implemented: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Reports/results updated: no.
- Retained evidence parsed or promoted: no.
- Live DB/checker execution run: no.
- Global leaderboard created: no.

## Next Safe Action

Human review of the U3 preflight fields and failure-bucket behavior, then authorize U4 local quality report v0 only if the preflight ledger schema is accepted.
