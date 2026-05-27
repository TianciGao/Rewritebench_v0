# 命令记录

前置确认：

```bash
pwd
git branch --show-current
git status -sb
```

已读取 project-control 文件：

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 80 project_control/MIGRATION_RUN_LOG.md
```

上下文检查：

```bash
find scripts -maxdepth 2 -type f | sort
find docs -maxdepth 2 -type f | sort
sed -n '1,180p' docs/README.md
sed -n '1,180p' scripts/env_all.example.sh
```

验证命令：

```bash
if command -v shellcheck >/dev/null 2>&1; then shellcheck scripts/setup_dev_env_ubuntu.sh scripts/check_dev_env.sh; else bash -n scripts/setup_dev_env_ubuntu.sh scripts/check_dev_env.sh; fi
if command -v shellcheck >/dev/null 2>&1; then echo shellcheck_available; else echo shellcheck_unavailable_bash_n_used; fi
pytest tests/pocr -q
pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q
git diff --check
python - <<'PY'
from pathlib import Path
paths = [
    Path('docs/dev_environment_zh.md'),
    *Path('audits/dev_environment_bootstrap_scripts_v0').glob('*.md'),
]
missing = [str(p) for p in paths if not p.exists() or not p.read_text(encoding='utf-8').strip()]
if missing:
    raise SystemExit('empty_or_missing_markdown=' + ','.join(missing))
print(f'markdown_non_empty={len(paths)}')
PY
git diff -U0 -- scripts/setup_dev_env_ubuntu.sh scripts/check_dev_env.sh docs/dev_environment_zh.md audits/dev_environment_bootstrap_scripts_v0 project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md | rg -n --ignore-case '(sk-[A-Za-z0-9_-]{20,}|api[_-]?key\s*=|authorization:\s*bearer|password\s*=|secret\s*=)' || true
git diff --cached --name-only | rg '^(output/|reports/|results/|cases/|runs/user/)|(^|/)skills\.md$|\.sql$|candidate_sql|project_control/MIGRATION_MASTER_PLAN\.md|project_control/DECISION_LOG\.md' || true
git diff --cached -U0 | rg -n --ignore-case '(sk-[A-Za-z0-9_-]{20,}|api[_-]?key\s*=|authorization:\s*bearer|password\s*=|secret\s*=)' || true
git status -sb
git diff --name-status
```

验证结果：

- `shellcheck` 不可用，`bash -n` 通过。
- changed Python modules：none；`py_compile` 不适用。
- `pytest tests/pocr -q`：`143 passed in 0.75s`。
- `pytest tests/user_entry/test_pocr_optional_user_run_integration.py tests/user_entry/test_cli_facade.py -q`：`31 passed in 0.15s`。
- Markdown non-empty：`markdown_non_empty=6`。
- Required phrase checks：通过。
- `git diff --check`：通过。
- Diff-only changed-file secret scan：通过；未新增凭证。
- Staged protected-path scan：通过。
- Staged secret scan：通过。
- Protected-path check：top-level `reports/` / `results/` / `cases/` / `runs/user` 无变更，既有 `output/` 未 staging。
