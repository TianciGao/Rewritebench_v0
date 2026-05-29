# Run Scope

Route:

- `method_id = sqlglot`
- `route_id = sqlglot_optimize_schema_aware`
- adapter command shape: `python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware`

Planned scope:

- Common-core v0 Track A same-engine local diagnostic.
- 40 cases x 3 engines = 120 planned rows.
- Engines: PostgreSQL, MySQL, Spark.

Executed timing scope:

- Timing used the prior execution/checker audit as an exact gate.
- Only rows with `exact_result_consistent=true` were timing-attempted.
- 66 rows were timing-attempted.
- 54 non-exact/frontier rows were not timed.

Runtime output:

- `/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/output/results/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/`
- `/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/output/logs/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/`
- `/tmp/sqlrb_sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/output/reports/sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0/`

No candidate generation, checker rerun beyond timing-required source/candidate execution, verifier pass, official metric computation, paper rendering, retained-evidence promotion, or leaderboard output was performed.
