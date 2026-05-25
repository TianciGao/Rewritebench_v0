# Command Log

- `pwd`
- `git branch --show-current`
- `git status -sb`
- `sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md`
- `sed -n '1,220p' project_control/MIGRATION_STATUS.md`
- `sed -n '1,260p' project_control/DECISION_LOG.md`
- `sed -n '1,220p' project_control/MIGRATION_RUN_LOG.md`
- `git worktree add --detach /tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree HEAD`
- `PYTHONPATH=/tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/src python -m cli.main user evaluate --case-set common_core_v0 --engines postgres,mysql,spark --adapter-command 'python baselines/sqlglot/sqlglot_user_adapter.py --route noop' --output-root /home/tianci_gao/code/Rewritebench_v0/output --run-id sqlglot_noop_track_a_120_user_reproduction_v0 --adapter-timeout 120 --enable-db-execution --enable-checker --collect-timing --timing-repetitions 2 --timing-timeout 30 --execution-timeout-sec 30`
- `PYTHONPATH=/tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/src python -m cli.main user compute-local-metrics --run-id-prefix sqlglot_noop_track_a_120_user_reproduction_v0 --engines postgres,mysql,spark --aggregate-run-id sqlglot_noop_track_a_120_user_reproduction_v0 --source-run-root /tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/runs/user --output-root /home/tianci_gao/code/Rewritebench_v0/output`
- `PYTHONPATH=/tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/src python -m cli.main user evaluate --case-set common_core_v0 --engines postgres,mysql,spark --adapter-command 'python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware' --output-root /home/tianci_gao/code/Rewritebench_v0/output --run-id sqlglot_optimize_schema_aware_track_a_120_user_reproduction_v0 --adapter-timeout 120 --enable-db-execution --enable-checker --collect-timing --timing-repetitions 2 --timing-timeout 30 --execution-timeout-sec 30`
- `PYTHONPATH=/tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/src python -m cli.main user compute-local-metrics --run-id-prefix sqlglot_optimize_schema_aware_track_a_120_user_reproduction_v0 --engines postgres,mysql,spark --aggregate-run-id sqlglot_optimize_schema_aware_track_a_120_user_reproduction_v0 --source-run-root /tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/runs/user --output-root /home/tianci_gao/code/Rewritebench_v0/output`
- `PYTHONPATH=/tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/src python -m cli.main user evaluate --case-set common_core_v0 --engines postgres,mysql,spark --adapter-command 'python baselines/calcite_hep_fail_closed/adapter.py' --output-root /home/tianci_gao/code/Rewritebench_v0/output --run-id calcite_hep_fail_closed_track_a_120_user_reproduction_v0 --adapter-timeout 120 --enable-db-execution --enable-checker --collect-timing --timing-repetitions 2 --timing-timeout 30 --execution-timeout-sec 30`
- `PYTHONPATH=/tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/src python -m cli.main user compute-local-metrics --run-id-prefix calcite_hep_fail_closed_track_a_120_user_reproduction_v0 --engines postgres,mysql,spark --aggregate-run-id calcite_hep_fail_closed_track_a_120_user_reproduction_v0 --source-run-root /tmp/sqlrb_nightly_user_repro_sqlglot_calcite_worktree/runs/user --output-root /home/tianci_gao/code/Rewritebench_v0/output`
- `python structured audit/output packaging script`
