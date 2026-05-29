# Command Log

本日志记录本任务命令。POCR 不是 official paper metric。POCR@planned 和 POCR@candidate 仍然是 D039 promotion views。POCR@curated 暂缓。Track A 120 不是 leaderboard。

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.

## 已执行

- `pwd`
- `git branch --show-current`
- `git status -sb --untracked-files=normal`
- `sed` / `tail` read of project-control files
- `find` read of required audit/source/test paths
- `sed` read of `src/cli/main.py`, `src/cli/pocr_diagnostic.py`, `src/sql_rewrite_bench/pocr/README.md`, `tests/user_entry/test_cli_facade.py`, and POCR aggregator tests
- `rg` search for old POCR wording
- `python -m py_compile src/cli/main.py src/cli/pocr_aggregate.py src/cli/pocr_diagnostic.py src/sql_rewrite_bench/user_output.py`
- `pytest tests/user_entry/test_cli_facade.py -q`
- `rg -n "POCR remains deferred|POCR=deferred|deferred pending external skill" src tests docs`
- `pytest tests/pocr -q`
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`
- Markdown non-empty and required phrase checks for docs, package README, and audit Markdown
- `git diff --check`
- `git diff --name-status`
- protected-path check for tracked changes under `cases/`, `skills.md`, candidate SQL, `runs/user`, `output/`, top-level `reports/`, top-level `results/`, paper/manuscript files

## 未执行

- no live API call
- no API key read
- no annotation JSONL generation
- no retry
- no pocr-diagnostic replay run
- no POCR aggregation production run
- no DB/checker/timing run
- no baseline rerun
- no candidate SQL generation or mutation
- no official POCR computation
- no paper-facing metric promotion

Changed-file secret scan、staged secret scan、final status 和 final diff 在 closeout 阶段追加执行。
