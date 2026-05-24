# R-Bot GPT-5.4 Bounded Live E2E Smoke

This packet records a bounded PostgreSQL-only live smoke for the adapted R-Bot GPT-5.4 route. It is local diagnostic evidence only and is not an original R-Bot paper reproduction.

Scope:
- route_id: `rbot_gpt54_adapted`
- method_id: `rbot`
- provider policy: OpenAI-compatible / GPTSAPI-compatible
- model: `gpt-5.4`
- selected rows: 6 PostgreSQL Common-core rows
- DB execution/checker/timing: enabled only for selected rows

Result summary:
- live calls attempted: 6
- candidates generated: 6
- candidate executable rows: 5
- checker exact rows: 5
- timed rows: 5
- fail-closed rows: 0
- execution-failed rows: 1 (`LONGTAIL_0011`)

Boundary:
- no official R-Bot runtime, RAG, Chroma, index build, or CalciteRewrite runtime was used
- no MySQL/Spark rows were selected
- no `compute-local-metrics`, SQLSolver, VeriEQL, official metrics, paper rendering, retained-evidence promotion, leaderboard, or Track A 120 run occurred

Next safe action: authorize a PostgreSQL-only R-Bot adapted bounded diagnostic over 20-40 rows with DB/checker/timing and local metrics. Do not run Track A 120 until a PG bounded diagnostic and route boundary policy are complete.
