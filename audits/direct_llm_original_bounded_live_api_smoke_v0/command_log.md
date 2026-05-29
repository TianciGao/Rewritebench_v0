# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 216aaf86042a4cbaf277e9416586ba625f939f8b HEAD
python -m cli.main user evaluate --help
python -m cli.main user compute-local-metrics --help
rg -n "D033|D034|D035" project_control/MIGRATION_MASTER_PLAN.md project_control/MIGRATION_STATUS.md project_control/DECISION_LOG.md
```

Project-control readback:

```bash
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
```

Safe live-env presence check:

```bash
python - <<'PY'
import os
for name in [
    "SQLRB_LLM_ALLOW_LIVE", "SQLRB_LLM_PROVIDER", "SQLRB_LLM_BASE_URL",
    "SQLRB_LLM_MODEL", "SQLRB_LLM_API_KEY", "GPTSAPI_API_KEY",
    "GPTSAPI_BASE_URL", "GPTSAPI_MODEL",
]:
    value = os.environ.get(name, "")
    if name.endswith("API_KEY"):
        state = "present" if value else "missing"
    elif name == "SQLRB_LLM_ALLOW_LIVE":
        state = "set_to_1" if value == "1" else ("set_not_1" if value else "missing")
    else:
        state = value if value else "missing"
    print(f"{name}={state}")
PY
```

Gate smoke:

```bash
printf 'CONS_0036\nPERF_0006\n' > /tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0_case_list.txt
env -u SQLRB_LLM_API_KEY -u GPTSAPI_API_KEY -u SQLRB_LLM_ALLOW_LIVE \
  SQLRB_LLM_PROVIDER=openai_compatible \
  SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1 \
  SQLRB_LLM_MODEL=gpt-5.4 \
  python -m cli.main user evaluate \
    --case-set common_core_v0 \
    --case-list /tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0_case_list.txt \
    --engines postgres,mysql,spark \
    --adapter-command "python baselines/direct_llm_original/adapter.py" \
    --output-root /tmp/sqlrb_direct_llm_original_bounded_live_api_smoke_v0/output \
    --run-id direct_llm_original_bounded_live_api_smoke_v0 \
    --enable-db-execution \
    --enable-checker
```

Validation:

```bash
pytest tests/user_entry/test_direct_llm_adapter.py -q
python -m py_compile baselines/direct_llm_original/adapter.py
git diff --check
git status -sb
```

No live provider call was made.
