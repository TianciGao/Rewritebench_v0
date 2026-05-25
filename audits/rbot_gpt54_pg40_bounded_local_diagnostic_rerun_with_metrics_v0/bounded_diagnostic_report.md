# Bounded Diagnostic Report

This packet records a PostgreSQL-only Common-core 40 rerun for `rbot_gpt54_adapted` using the adapted GPT-5.4 live path. It replaces the missing-source-run situation from the prior PG40 audit by preserving a new run id: `rbot_gpt54_pg40_bounded_diagnostic_rerun_v0`.

Selected-row rationale: all Common-core v0 PostgreSQL rows were selected, and no MySQL/Spark rows were run.

Provider status: live gate enabled, provider policy `openai_compatible`, model `gpt-5.4`; no raw API key values were printed, written, staged, or committed.

Generation/extraction/preflight summary:

- selected rows: `40`
- live calls / generated candidates: `40`
- preflight passed: `40`
- fail-closed rows: `0`

DB/checker/timing summary:

- source executable: `40`
- candidate executable: `38`
- exact: `37`
- mismatch: `1`
- candidate execution failed: `2`
- timed exact rows: `33`

Local metrics summary from `local_metrics.py`:

- generation rate: `1.0`
- execution coverage: `0.95`
- result consistency: `0.925`
- GM speedup: `0.9777997901126648`
- P10/P25/P50/P75/P90: `0.5865455274023522` / `0.9845480112740764` / `0.9998615395796396` / `1.0142327268706417` / `1.5983027547333224`

Failure buckets:

- `candidate_execution_failed`: `2`
- `mismatch`: `1`
- `none`: `37`

Previous frontier rows: `PORT_0013` remains mismatch; `LONGTAIL_0011` remains candidate execution failed; `PERF_0013` is now exact/timed; `PERF_0008` is the new candidate execution failure.

Source-like/no-op behavior: source-like count is `0`. All generated candidates were marked `changed` by the local ledger, so this remains a diagnostic classification only and not POCR.

Route readiness: the rerun is stable enough to write an R-Bot adapted PostgreSQL route boundary/policy packet. It is not sufficient to authorize Track A 120 by itself because MySQL/Spark were not run and this remains a bounded PG40 local diagnostic.

This is adapted GPT-5.4 local diagnostic evidence only. It is not original R-Bot paper reproduction, not official metrics, not official SER, not paper result input, not retained evidence promotion, and not leaderboard input.
