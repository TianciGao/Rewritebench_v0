# Live E2E Report

This packet records a bounded live Repair-1 end-to-end smoke over 3 selected actionable Direct LLM original frontier rows.

Selected rows:

- `CONS_0005` / `postgres` / `CONS`: `checker_mismatch_feedback` (PostgreSQL mismatch feedback row; minimal same-engine repair smoke for checker mismatch.)
- `PERF_0062` / `mysql` / `PERF`: `checker_mismatch_feedback` (MySQL PERF mismatch feedback row; adds engine/pool diversity for checker mismatch.)
- `LONGTAIL_0012` / `spark` / `LONGTAIL`: `candidate_execution_error_feedback` (Spark LONGTAIL candidate_execution_failed feedback row; covers execution-error repair path.)

Provider preflight:

- `SQLRB_LLM_ALLOW_LIVE=1`: present by presence/equality check.
- Provider env presence: provider, base URL, model, and API key env were present by presence-only check.
- Provider health check: `/v1/models` returned HTTP 200 and listed the configured model.
- Provider used by adapter metadata: `openai_compatible` on host `api.gptsapi.net`, model `gpt-5.4`.
- Secret values were not printed or written.

Generation and extraction summary:

- selected rows: 3
- live call attempts: 3
- repaired candidates generated: 3
- extraction status: `extracted=3`
- preflight passed: 3
- fail-closed rows: 0

DB/checker/timing summary:

- source executable rows: 3
- candidate executable rows: 3
- checker success rows: 3
- exact rows: 3
- timed rows: 3

Failure summary:

- exact rows: 3
- mismatch rows after Repair-1 smoke: 0
- candidate execution failed rows after Repair-1 smoke: 0
- fail-closed rows: 0

Boundary:

This is a bounded local diagnostic smoke only. It is not Track A 120, not aggregate local metrics, not official metrics, not official SER, not verifier evidence, not retained evidence promotion, and not a paper result.

Next safe action: authorize a 13-actionable-row live Repair-1 diagnostic run with DB/checker/timing. Do not run Repair-1 Track A 120 until the 13-row actionable diagnostic passes and a 120-route assembly policy is written.
