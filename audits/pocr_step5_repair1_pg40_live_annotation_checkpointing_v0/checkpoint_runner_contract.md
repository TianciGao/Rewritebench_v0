# Checkpoint Runner Contract

`src/sql_rewrite_bench/pocr/checkpointed_annotation_runner.py` is a bounded diagnostic Stage A annotation runner.

Contract summary:

- It resolves existing candidate SQL read-only.
- It writes a manifest row with `call_status=pending` before each provider call.
- It updates each row after completion to `schema_valid`, `schema_invalid`, `malformed_json`, `provider_call_failed`, `timeout`, `skipped_existing`, `skipped_no_candidate`, `skipped_no_skills`, or `prompt_build_failed`.
- It writes `annotation_manifest.csv`, `annotation_schema_validation.csv`, `prompt_manifest.csv`, `provider_call_manifest.csv`, `checkpoint_state.json`, and `safe_annotation_outputs.jsonl` under D035-style `output/results/<run_id>/...` local output paths.
- It skips existing `schema_valid` rows with matching `candidate_sha256` unless `--force` is used.
- It retries failed rows only with `--retry-failed`.
- It fail-closes candidate SHA mismatches and duplicate JSONL rows.
- It records only safe provider metadata and never serializes API key values.
- It does not compute official POCR, route-level POCR, paper metrics, or a leaderboard.
