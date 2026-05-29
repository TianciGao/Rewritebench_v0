# POCR User Diagnostic Output Contract

This packet records the user-output-compatible diagnostic POCR scaffold added for `pocr_user_diagnostic_output_contract_v0`.

The implementation adds row-level diagnostic output objects, a D035-style writer, and a thin POCR user facade under `src/sql_rewrite_bench/pocr/`. The facade is default-off and offline: with `live_enabled=false` and no annotation JSONL, it emits `annotation_missing` diagnostic rows and does not call any API.

Boundaries:
- Positive Operation Coverage diagnostic support only.
- This is not official POCR.
- Stage A annotation alone is not counted.
- Stage B transformation-aware validation is diagnostic only.
- Semantic guard atoms are not part of operation coverage numerator.
- No route-level POCR score is emitted.
- No paper metric is promoted and no leaderboard is created.

Sample audit files in this packet were generated from four existing Direct LLM original PostgreSQL candidate rows using no annotation JSONL, so all sample rows have `annotation_status=annotation_missing`.

Next safe action: wire the POCR diagnostic facade into an optional user-run flow, or run one more selected route through the same diagnostic contract.
