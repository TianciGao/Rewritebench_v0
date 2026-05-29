# Future Minimal Split Prompt

Task title:
U2 minimal implementation of user-entry resolver, adapter-runner, and ledger-writer split

Purpose:
Implement only the behavior-preserving extraction designed in `audits/user_entry_module_split_design_v0/`.

Allowed implementation scope:

- Add `src/sql_rewrite_bench/case_package_resolver.py`.
- Add `src/sql_rewrite_bench/adapter_runner.py`.
- Add `src/sql_rewrite_bench/user_ledger.py`.
- Update `src/sql_rewrite_bench/user_run.py` only to delegate to those modules.
- Update `tests/user_entry/` only for behavior-preservation coverage.
- Update user-entry audit/project-control outputs if required by the implementation task.

Hard boundaries:

- Do not implement candidate preflight.
- Do not implement local quality reports.
- Do not implement tag-aware slices.
- Do not implement timing diagnostics.
- Do not compute official metrics.
- Do not render paper tables.
- Do not update reports/results.
- Do not parse retained evidence.
- Do not change case sets, denominators, paper results, case membership, or raw legacy evidence.
- Do not create a global leaderboard.

Required behavior preservation:

- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help` passes.
- `python scripts/user/run_user_benchmark.py --help` passes.
- Public `--smoke --dry-run` still passes.
- Public `--smoke` adapter-capture still passes.
- Existing user-entry tests pass.
- Outputs remain under `runs/user/{run_name}/`.
- Generated validation outputs are removed before commit.

Recommended implementation sequence:

1. Add resolver and tests.
2. Add adapter runner and tests.
3. Add ledger writer and tests.
4. Rewire `user_run.py` with minimal behavior changes.
5. Run validation gates and protected-surface checks.

Do not combine this task with U3 candidate preflight or any metrics/reporting work.
