# Live 13-Row Diagnostic Report

This packet records a bounded live Repair-1 diagnostic over exactly the 13 actionable Direct LLM original frontier rows.

Selected row rationale:

- `CONS_0005` / `postgres` / `CONS`: `checker_mismatch_feedback` from `mismatch` frontier
- `CONS_0005` / `mysql` / `CONS`: `checker_mismatch_feedback` from `mismatch` frontier
- `CONS_0037` / `mysql` / `CONS`: `checker_mismatch_feedback` from `mismatch` frontier
- `PERF_0062` / `mysql` / `PERF`: `checker_mismatch_feedback` from `mismatch` frontier
- `PORT_0004` / `mysql` / `PORT`: `checker_mismatch_feedback` from `mismatch` frontier
- `PORT_0012` / `mysql` / `PORT`: `checker_mismatch_feedback` from `mismatch` frontier
- `PORT_0013` / `mysql` / `PORT`: `checker_mismatch_feedback` from `mismatch` frontier
- `PORT_0022` / `mysql` / `PORT`: `checker_mismatch_feedback` from `mismatch` frontier
- `PORT_0024` / `mysql` / `PORT`: `checker_mismatch_feedback` from `mismatch` frontier
- `CONS_0005` / `spark` / `CONS`: `checker_mismatch_feedback` from `mismatch` frontier
- `CONS_0009` / `spark` / `CONS`: `candidate_execution_error_feedback` from `candidate_execution_failed` frontier
- `CONS_0011` / `spark` / `CONS`: `candidate_execution_error_feedback` from `candidate_execution_failed` frontier
- `LONGTAIL_0012` / `spark` / `LONGTAIL`: `candidate_execution_error_feedback` from `candidate_execution_failed` frontier

Unsupported exclusion boundary:

The five unsupported-engine Spark rows were excluded and not attempted:

- `PORT_0008` / `spark` / `PORT`
- `PORT_0012` / `spark` / `PORT`
- `PORT_0022` / `spark` / `PORT`
- `PORT_0024` / `spark` / `PORT`
- `PORT_0025` / `spark` / `PORT`

Provider status:

- `SQLRB_LLM_ALLOW_LIVE=1`: present by presence/equality check.
- Provider, base URL, model, and API key env: present by presence-only check.
- Safe provider health check: `/v1/models` returned HTTP 200 and listed the configured model.
- Adapter metadata recorded provider `openai_compatible`, host `api.gptsapi.net`, model `gpt-5.4`, and `live_call=true` for selected rows.
- No secret values were printed or written.

Generation/extraction/preflight summary:

- selected rows: 13
- live calls: 13
- repaired candidates generated: 13
- extraction passed: 13
- preflight passed: 13
- fail-closed rows: 0

DB/checker/timing summary:

- source executable rows: 13
- candidate executable rows: 13
- exact rows: 9
- mismatch rows: 4
- candidate execution failed rows: 0
- timed rows: 9

The four remaining mismatches are selected-row local diagnostic outcomes only. They are not official route metrics and are not paper-facing results.

This is not Track A 120: it uses only the 13 actionable Direct LLM original frontier rows and excludes the five unsupported-engine rows. It does not select the full 40 cases x 3 engines denominator.

This is not official metrics: `compute-local-metrics` was not run, no verifier was run, no official SER was computed, no paper report/result changed, no retained evidence was promoted, and no leaderboard was created.

Next safe action: write a Repair-1 Track A 120 route assembly policy before running the full Repair-1 120 canonical local diagnostic.
