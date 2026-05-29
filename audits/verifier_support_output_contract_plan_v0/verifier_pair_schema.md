# Verifier Pair Schema

`verifier_pairs.csv` records planned verifier pairs.

Required columns:

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

Allowed `pair_type` values:

- `source_vs_candidate`
- `source_vs_positive`
- `source_vs_hard_negative`
- `source_vs_candidate_port_target`
- `support_pair_smoke`

Notes:

- `positive_sql_path` is nullable unless the pair type uses a positive reference.
- `negative_sql_path` is nullable unless the pair type uses a hard-negative reference.
- Hard-negative checker controls must remain separate from user method candidates.
- PORT target-engine pairs require explicit role metadata before use.
- Pair planning must not infer roles from filenames or SQL text.
