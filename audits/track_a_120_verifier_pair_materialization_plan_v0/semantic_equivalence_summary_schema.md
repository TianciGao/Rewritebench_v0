# Semantic Equivalence Summary Schema

Future verifier-phase outputs should be written under a verifier output subtree, for example `output/results/<run_id>/verifier/`, `output/logs/<run_id>/verifier.log`, and `output/reports/<run_id>/verifier_boundary.md`.

## `verifier/semantic_equivalence_summary.json`

Required fields:

- `route_id`
- `run_id`
- `tool`
- `eligible_exact_pairs`
- `attempted_pairs`
- `equivalent`
- `non_equivalent`
- `unknown`
- `timeout`
- `unsupported`
- `not_implemented`
- `tool_error`
- `no_verifier_support`
- `not_attempted`
- `decidable_pairs`
- `SER`
- `SER_status`: one of `computed`, `coverage_limited`, `N.A.`
- `boundary_notes`

`SER` may be non-null only when formal verifier evidence produces at least one decidable pair and the route/scope has approval to interpret that evidence. Unknown, timeout, unsupported, not-implemented, tool-error, no-verifier-support, and not-attempted outcomes are reported separately and excluded from the decidable denominator.

## `verifier/verifier_verdicts.jsonl`

One JSON object per tool/pair attempt, including identity guard records and source-vs-candidate records. Required row fields include `pair_id`, `route_id`, `run_id`, `tool`, `engine`, `case_id`, `pair_role`, `identity_guard_role`, `source_sql_sha256`, `candidate_sql_sha256`, `schema_ref`, `raw_verdict`, `normalized_verdict`, `runtime_ms`, `timeout_seconds`, `artifact_paths`, and boundary flags.

## `verifier/verifier_by_engine.csv`

Columns should include `route_id`, `run_id`, `tool`, `engine`, `eligible_exact_pairs`, `attempted_pairs`, verdict counts, `decidable_pairs`, `SER`, `SER_status`, and `boundary_notes`.

## `verifier/verifier_by_pool.csv`

Columns should include `route_id`, `run_id`, `tool`, `pool`, `eligible_exact_pairs`, `attempted_pairs`, verdict counts, `decidable_pairs`, `SER`, `SER_status`, and `boundary_notes`.

## `verifier/verifier_boundary.md`

Must state whether the run is local-only, whether SQLSolver or VeriEQL actually ran, whether identity guards passed, whether SER is computed or coverage-limited/N.A., and that verifier limitations are not method rewrite failures.
