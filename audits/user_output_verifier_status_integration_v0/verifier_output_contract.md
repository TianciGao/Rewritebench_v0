# Verifier Output Contract

## `verifier_status.json`

Expected fields:

- `schema_version`
- `run_id`
- `verifier_enabled`
- `verifier_tools_requested`
- `verifier_tools_completed`
- `semantic_equivalence_rate_status`
- `official_SER`
- `result_checker_exactness_used`
- `local_diagnostic_only`
- `paper_result_input`
- `retained_evidence_promoted`
- `leaderboard_input`
- `tool_summaries`
- `boundary_notes`

Allowed `semantic_equivalence_rate_status` values:

- `N.A.`
- `coverage_limited`
- `computed_local_support`

## `semantic_equivalence_summary.json`

When present, the exporter uses it only as existing verifier-support evidence. It does not run verifier tools and does not compute official SER. If no explicit `verifier_status.json` exists, summary counts can populate a normalized `verifier_status.json`.

## Boundary

Verifier-support statuses are separate from method failure buckets. `coverage_limited`, `no_verifier_support`, `unsupported`, `unknown`, `timeout`, and `tool_error` describe verifier-support coverage or tool behavior. They are not rewrite-method failures and they do not replace local result-checker exactness or local metrics.
