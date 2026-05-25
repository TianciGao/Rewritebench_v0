# POCR User Annotation JSONL Replay v0

This packet records default-off user-run annotation JSONL replay support for diagnostic POCR. The implementation accepts `--annotation-jsonl` only with `--enable-pocr-diagnostic`, reads existing JSONL annotations offline, validates mapping/schema conservatively, and writes only D035-shaped diagnostic user outputs under a caller-provided output root.

Replay smoke used the existing Direct LLM PG40 annotation artifact and the existing Direct LLM PostgreSQL candidate SQL root. Because the requested user replay route ID differs from the original annotation artifact route ID, all 40 rows failed closed as `schema_invalid` route-mismatch diagnostics. This is expected under the conservative mapping policy and is not an official POCR result.

No live API call, API-key read, DB/checker/timing run, baseline rerun, official POCR computation, route-level POCR aggregation, paper metric promotion, or leaderboard output occurred.
