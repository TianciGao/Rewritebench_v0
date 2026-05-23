# verieql_internal_state_schema_probe_v0

Audit date: 2026-05-23

Branch: `feature/case-package-v2-external-schema`

## Verdict

VeriEQL timeout-mode state semantics explain the repeated `EQU` states followed by `TMO` seen for the minimal equivalent synthetic pair. The batch timeout runner increases the finite bound after each `EQU`; if the next bound exceeds the tool timeout, it appends `TMO`. This means `EQU...TMO` is a finite-bound progress history, not a clean final equivalence verdict.

The current release wrapper should continue normalizing any row containing `TMO` to `timeout` for SQL-RewriteBench local verifier-support output. Do not reinterpret partial `EQU+TMO` as formal equivalence evidence.

## Scope

This task inspected VeriEQL source, shipped benchmark JSONL examples, historical VeriEQL output files, and prior local canary audits. It did not run Common-core, SQLSolver, new real-case canaries, official metrics, paper reports, retained-evidence promotion, or leaderboard output.

## Files

- `state_semantics_review.md`
- `jsonl_schema_expectation_review.md`
- `constraint_schema_gap_review.md`
- `equivalent_timeout_hypotheses.md`
- `builtin_examples_review.md`
- `recommendation.md`
- `command_log.md`
- `protected_surface_check.md`
- `boundary_checklist.md`
