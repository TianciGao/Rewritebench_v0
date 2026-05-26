# Manual Review Policy

Manual review rows are CSV hooks, not UI and not diagnostic-result mutations.

Review actions are limited to:
- `inspect_candidate_source_diff`;
- `inspect_prompt_output`;
- `retry_annotation`;
- `keep_fail_closed`;
- `mark_manual_note_only`.

Manual review rows keep `diagnostic_only=true` and `official_pocr_computed=false`. They do not compute official POCR, route-level POCR, paper metrics, or leaderboard entries.
