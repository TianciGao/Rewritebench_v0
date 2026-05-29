# Run Scope

Rerun scope:

- Engine: PostgreSQL only.
- Case set: Common-core v0 PostgreSQL slice.
- Selected rows: 40.
- Baseline family: Calcite.
- Method/route: `calcite_hep_fail_closed`.

External runtime:

- `SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke`
- `SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep`
- `SQLRB_CALCITE_HEP_TIMEOUT=30`

PostgreSQL execution environment:

- Loaded from `scripts/env_postgres.local.sh`.
- Verified by `scripts/dev/check_local_engine_env.py --engine postgres`.

Out of scope:

- MySQL and Spark.
- Full 120 Track-A rows.
- Direct LLM and Repair-1.
- SQLSolver and VeriEQL.
- Official metrics.
- Semantic Equivalence Rate.
- Formal Regression@20.
- Paper reports/results.
- Retained evidence promotion.
- Leaderboard output.
