# R-Bot GPT-5.4 PG40 Bounded Local Diagnostic

This packet records a PostgreSQL-only Common-core 40 bounded local diagnostic for the adapted R-Bot GPT-5.4 route.

Scope:
- route_id: `rbot_gpt54_adapted`
- method_id: `rbot`
- engine: PostgreSQL only
- selected rows: 40 Common-core PostgreSQL rows
- live provider: OpenAI-compatible / GPTSAPI-compatible
- model: `gpt-5.4`
- DB execution, checker, and timing: enabled only for selected PostgreSQL rows

Evaluate result:
- selected: 40
- generated: 40
- candidate executable: 38
- exact: 37
- mismatch: 1
- candidate execution failed: 2
- timed: 33
- source-like/no-op diagnostic count: 0

`compute-local-metrics` was attempted with the requested command shape but failed before producing metric outputs because the aggregate run directory already contained non-aggregate evaluate artifacts. No local metric rates were hand-computed.

This is adapted local diagnostic evidence only, not original R-Bot paper reproduction, not Track A 120, not official metrics, and not paper evidence.
