# Interpretation Notes

This rerun uses `examples/user/noop_adapter.py`, which copies source SQL into the candidate path. Exact rows therefore mean only local source-like diagnostic equivalence for rows where source and candidate execute in the same role/engine shape.

For PORT cross-dialect rows, the no-op adapter is not a valid target-generating method. The current failures are target-candidate execution failures after successful source-reference execution:

- PostgreSQL target run: five MySQL-source PORT candidates fail in PostgreSQL.
- MySQL target run: four PostgreSQL-source PORT candidates fail in MySQL.

This is not a regression of the controlled PORT cross-dialect path. Controlled target-reference adapters already validated the target execution and checker handoff separately, with forward exact 5/5 and reverse exact 4/4.

This audit does not convert exact counts into official accuracy, metric, paper, or leaderboard claims.
