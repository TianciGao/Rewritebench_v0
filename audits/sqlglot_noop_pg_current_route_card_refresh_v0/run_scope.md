# Run Scope

Scope:

- case set: `common_core_v0`
- engine: `postgres`
- selected rows: 40
- method_id: `sqlglot_noop`
- route_id: `sqlglot_noop`
- baseline family: `sqlglot`

Stages run:

1. Candidate generation/capture over all 40 selected PostgreSQL rows.
2. PostgreSQL execution/checker over generated candidates.
3. Exact-gated timing over exact/result-consistent rows only.
4. Local diagnostic route-card projection.

Runtime root:

- `/tmp/sqlrb_sqlglot_noop_pg_current_route_card_refresh_v0/`

D035-shaped runtime subroots:

- `/tmp/sqlrb_sqlglot_noop_pg_current_route_card_refresh_v0/output/results/sqlglot_noop_pg_current_route_card/`
- `/tmp/sqlrb_sqlglot_noop_pg_current_route_card_refresh_v0/output/logs/sqlglot_noop_pg_current_route_card/`
- `/tmp/sqlrb_sqlglot_noop_pg_current_route_card_refresh_v0/output/reports/sqlglot_noop_pg_current_route_card/`

Excluded work:

- no MySQL or Spark rows
- no all-120 Track-A run
- no Calcite rerun
- no Direct LLM or Repair-1
- no SQLSolver or VeriEQL
- no official metrics
- no Semantic Equivalence Rate
- no formal Regression@20
- no top-level reports/results update
- no retained-evidence promotion
- no leaderboard output
