# Verifier Verdict Schema

`verifier_verdicts.jsonl` records one JSON object per attempted or planned verifier pair.

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
- `local_diagnostic_only`
- `official_metric_input`
- `paper_result_input`
- `retained_evidence_promoted`
- `leaderboard_input`

Allowed `verdict` values:

- `equivalent`
- `non_equivalent`
- `unknown`
- `timeout`
- `unsupported`
- `tool_error`
- `not_attempted`

Normalization policy:

- Tool-native outputs must be mapped to the allowed verdict vocabulary.
- `equivalent` and `non_equivalent` are decidable outcomes.
- `unknown`, `timeout`, `unsupported`, `tool_error`, and `not_attempted` are reported separately and are not silently dropped.
- Raw stdout/stderr paths must point under `output/results/<run_id>/verifier/tools/<tool>/<pair_id>/` or `output/logs/<run_id>/`.
- Credentials and private paths must not be copied into public-facing logs.
