# Command Log

Preflight:

```text
git status -sb
git branch --show-current
git fetch origin
git merge-base --is-ancestor ea2d52f HEAD
git show origin/main:<project-control files>
git show origin/feature/case-package-v2-external-schema:<project-control files>
rg for D033/D034/D035 in origin feature DECISION_LOG
rg for User-Agent fix in adapter/test
tracked-file secret scan
staged protected-artifact check
```

Important preflight observations:

```text
branch=feature/case-package-v2-external-schema
ea2d52f_in_HEAD=yes
origin_feature_contains_D033_D034_D035=yes
origin_main_contains_D033_D034_D035=no
adapter_exists=yes
adapter_user_agent_fix_present=yes
tracked_secret_scan=passed
staged_protected_runtime_artifacts=no
```

Smoke:

```text
started_at=2026-05-24T14:57:56Z
ended_at=2026-05-24T14:58:32Z
exit_code=0
http_403_code_1010_detected=0
```

Validation commands:

```bash
pytest tests/user_entry/test_direct_llm_adapter.py -q
python -m py_compile baselines/direct_llm_original/adapter.py
git diff --check
git status -sb
```

