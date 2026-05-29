# Live E2E Report

The smoke selected six PostgreSQL Common-core rows: `PERF_0006`, `CONS_0036`, `PERF_0007`, `CONS_0005`, `CONS_0007`, and `LONGTAIL_0011`. This covers the required `PERF_0006/postgres`, `CONS_0036/postgres`, an additional PERF row, multiple CONS rows, and one LONGTAIL row with available schema context.

Provider status:
- live gate enabled
- provider policy: OpenAI-compatible / GPTSAPI-compatible
- model: `gpt-5.4`
- live calls attempted: 6
- live calls outside selected rows: 0
- raw response saving: disabled

Generation/extraction/preflight summary:
- candidates generated: 6/6
- single-SQL extraction passed: 6/6
- candidate preflight passed: 6/6
- fail-closed rows: 0

DB/checker/timing summary:
- DB execution attempted only for selected PostgreSQL rows
- source executable: 6/6
- candidate executable: 5/6
- checker exact: 5/5 attempted
- timed rows: 5/6 selected rows, 5/5 exact executable rows

Failure summary:
- exact rows: 5
- mismatch rows: 0
- candidate execution failed rows: 1 (`LONGTAIL_0011`)
- fail-closed rows: 0

`LONGTAIL_0011` generated a candidate that PostgreSQL rejected because nested window-function calls are not allowed. This is a bounded live-smoke failure frontier item, not a paper metric and not official R-Bot evidence.

Boundary:
- This is an adapted GPT-5.4 local diagnostic route, not an original R-Bot paper reproduction.
- The official R-Bot runtime, RAG index, Chroma, and CalciteRewrite runtime were not invoked.
- This is not Track A 120 and not official metrics.

Next safe action: authorize a PostgreSQL-only R-Bot adapted bounded diagnostic over 20-40 rows with DB/checker/timing and local metrics. Do not run Track A 120 until the bounded diagnostic and route boundary policy are complete.
