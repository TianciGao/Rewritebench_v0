# Docs And Examples Gap Review

Examples:

- `examples/user/noop_adapter.py`
- `examples/user/port_mysql_target_reference_adapter.py`
- `examples/user/port_postgres_target_reference_adapter.py`
- `examples/user/port_spark_target_reference_adapter.py`

The examples directory exists and contains adapter examples. A future examples cleanup should add or update a minimal runnable sample that shows `sqlrb user evaluate` producing D035 `output/results|logs|reports/<run_id>/` exports.

Docs:

- Current docs are mostly root-level files under `docs/*.md`.
- Development docs live under `docs/dev/`.
- D035 target subdirectories `docs/guide/`, `docs/spec/`, and `docs/templates/` do not exist yet.

Outdated wording:

- `docs/USER_BENCHMARK_GUIDE.md`, `docs/USER_ENTRY_DATA_FLOW.md`, `docs/LOCAL_ENGINE_SETUP.md`, `docs/RUN_ARTIFACT_POLICY.md`, and `baselines/sqlglot/README.md` still describe `runs/user/<run_id>/` as the user-run output root.
- That wording is accurate for the internal source-run staging layer, but incomplete for the current user-facing facade because `src/cli` exports to D035 output roots.

Recommended docs cleanup:

- Add `docs/guide/` for user-facing guide material.
- Add `docs/spec/` for output contract and adapter/verifier specs.
- Add `docs/templates/` for adapter and output templates if needed.
- Update user docs to distinguish:
  - internal source-run staging: `runs/user/<run_id>/`
  - user-facing exported output: `output/results|logs|reports/<run_id>/`

No docs were modified in this task.
