# User CLI And Output Readiness

Current public facade:

- `src/cli/`
- command shape: `sqlrb user ...` or `python -m cli.main user ...`

Current output contract:

- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

Internal transitional staging:

- `runs/user/<run_id>/`
- staging only, not the public output contract.

Readiness:

- SQLGlot noop and SQLGlot optimize can be invoked with `--adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route ..."` through the user facade.
- Calcite HEP can be invoked with `--adapter-command "python baselines/calcite_hep_fail_closed/adapter.py"` and external Calcite env vars.
- Direct LLM routes do not yet have D035 user-facing adapter contracts.
- Verifier facade exists for synthetic smoke, but not for exact candidate `run-candidates`.

Output protection:

- Top-level `reports/` and `results/` remain official/paper surfaces.
- User diagnostic reruns must not update them.
