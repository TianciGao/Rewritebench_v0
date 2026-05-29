# Command Log

Preflight and context:

- `git status -sb && git branch --show-current && git log --oneline -8`
- Read required project-control files.
- Read `audits/real_user_adapter_evaluation_plan_v0/`.
- Read `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/`.
- Read `baselines/sqlglot/README.md`.
- Read `baselines/sqlglot/sqlglot_user_adapter.py`.

Dependency and environment:

- `source ~/code/sql-rewrite-bench/.venv/bin/activate && python - <<'PY' ... import sqlglot ... PY`
- `source ~/code/sql-rewrite-bench/.venv/bin/activate && source scripts/env_postgres.local.sh && source scripts/env_mysql.local.sh && source scripts/env_spark.local.sh && export PYTHONPATH=src && python scripts/dev/check_local_engine_env.py`

Case lists:

- `/tmp/sqlrb_sqlglot_same_engine_smoke.txt`: `PERF_0006`, `CONS_0005`.
- `/tmp/sqlrb_sqlglot_port_pg_probe.txt`: `PORT_0004`.
- `/tmp/sqlrb_sqlglot_port_mysql_probe.txt`: `PORT_0003`.

Phase A adapter-capture runs:

- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_noop_capture_pg_smoke`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" --out runs/user/sqlglot_optimize_capture_pg_smoke`

Phase B same-engine DB/checker runs:

- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_noop_pg_bounded_smoke --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" --out runs/user/sqlglot_optimize_pg_bounded_smoke --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_noop_mysql_bounded_smoke --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" --out runs/user/sqlglot_optimize_mysql_bounded_smoke --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_noop_spark_bounded_smoke --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_sqlglot_same_engine_smoke.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route optimize" --out runs/user/sqlglot_optimize_spark_bounded_smoke --enable-db-execution --enable-checker`

Phase C PORT probe:

- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_sqlglot_port_pg_probe.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_noop_port_pg_target_probe --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --case-list /tmp/sqlrb_sqlglot_port_mysql_probe.txt --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" --out runs/user/sqlglot_noop_port_mysql_target_probe --enable-db-execution --enable-checker`
- Optimize PORT probe was skipped because optimize route Phase B did not fully succeed.

Validation:

- Project-control readability check.
- Audit Markdown/CSV/JSON sanity checks.
- `git diff --check`.
- Protected-surface diff check.
- Git status/staging check confirming no `runs/user/` outputs are staged or committed.
