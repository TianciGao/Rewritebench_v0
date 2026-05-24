# SQLGlot Optimize Schema-Aware Track A 120 Canonical User Rerun

Task: `sqlglot_optimize_schema_aware_track_a_120_canonical_user_rerun_v0`

Branch: `feature/case-package-v2-external-schema`

Run id: `sqlglot_optimize_schema_aware_track_a_120_canonical_v0`

Route:
- `route_id = sqlglot_optimize_schema_aware`
- `method_id = sqlglot`
- adapter command: `python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware`

Verdict:
- The rerun used the D035 user facade.
- Multi-engine evaluate produced three per-engine source runs.
- Canonical aggregate metrics were computed through `python -m cli.main user compute-local-metrics`, which delegates to `src/sql_rewrite_bench/local_metrics.py`.
- Canonical metrics artifacts exist in the aggregate source run and D035 exported output.
- This remains local diagnostic output only; it is not official metrics, paper evidence, retained evidence, or leaderboard input.
