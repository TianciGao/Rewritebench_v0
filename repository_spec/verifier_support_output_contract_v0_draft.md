# Verifier Support Output Contract v0 Draft

Status: draft design only.

This draft defines the future local-output contract for VeriEQL and SQLSolver support in SQL-RewriteBench user-facing local runs.

It does not implement VeriEQL, SQLSolver, verifier invocation, Semantic Equivalence Rate computation, official metrics, reports/results updates, retained-evidence promotion, paper rendering, or leaderboard output.

## Role

VeriEQL and SQLSolver are verifier/support tools. They do not generate rewritten SQL and must not be ranked against rewrite methods or included in same-engine speedup tables.

Semantic Equivalence Rate remains `N.A.` unless formal verifier evidence exists.

## Output Placement

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  semantic_equivalence_summary.json
  tools/
    verieql/
    sqlsolver/

output/logs/<run_id>/verifier.log
output/reports/<run_id>/verifier_summary.md
```

## Pair Types

- `source_vs_candidate`
- `source_vs_positive`
- `source_vs_hard_negative`
- `source_vs_candidate_port_target`
- `support_pair_smoke`

Hard-negative checker controls must remain separate from user method candidates.

## verifier_pairs.csv

Required fields:

- `pair_id`
- `run_id`
- `tool`
- `case_id`
- `pool`
- `engine`
- `route_id`
- `method_id`
- `pair_type`
- `source_sql_path`
- `candidate_sql_path`
- `positive_sql_path`
- `negative_sql_path`
- `schema_context_path`
- `checker_context_path`
- `denominator_id`
- `local_diagnostic_only`
- `official_metric_input`
- `paper_result_input`
- `retained_evidence_promoted`
- `leaderboard_input`

## verifier_verdicts.jsonl

Required fields:

- `pair_id`
- `tool`
- `tool_version`
- `invocation_status`
- `verdict`
- `raw_stdout_path`
- `raw_stderr_path`
- `runtime_ms`
- `timeout_seconds`
- `normalized_verdict`
- `verdict_reason`
- `artifact_paths`
- local-only boundary flags

Allowed verdicts:

- `equivalent`
- `non_equivalent`
- `unknown`
- `timeout`
- `unsupported`
- `tool_error`
- `not_attempted`

## semantic_equivalence_summary.json

Required fields:

- `run_id`
- `verifier_tools_requested`
- `verifier_tools_completed`
- `pairs_planned`
- `pairs_attempted`
- `equivalent_count`
- `non_equivalent_count`
- `unknown_count`
- `timeout_count`
- `unsupported_count`
- `tool_error_count`
- `decidable_count`
- `semantic_equivalence_rate`
- `verifier_decidability_rate`
- `na_reason`
- local-only boundary flags

`decidable_count = equivalent_count + non_equivalent_count`.

`semantic_equivalence_rate = equivalent_count / decidable_count` only when `decidable_count > 0`; otherwise it is `N.A.` with `na_reason`.

## Boundary

Local verifier outputs are not official metrics, paper results, retained evidence, or leaderboard input. Promotion requires a separate authorized task.
