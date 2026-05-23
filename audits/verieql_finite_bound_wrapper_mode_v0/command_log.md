# Command Log

## Preflight

```bash
git status -sb
git branch --show-current
git merge-base --is-ancestor bc72cf1 HEAD
git fetch origin main feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D032|D033|D034|D035" project_control/DECISION_LOG.md
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```

## Implementation Reads

```bash
sed -n '1,620p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '620,1040p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '1,380p' tests/user_entry/test_verieql_support.py
rg -n "verieql|VeriEQL|verifier_support|semantic_equivalence|normalize" tests src/sql_rewrite_bench/verifier_support -g '*.py'
```

## Test And Smoke Commands

```bash
pytest tests/user_entry/test_verieql_support.py -q
python -m py_compile src/sql_rewrite_bench/verifier_support/verieql.py
pytest tests/user_entry -q
```

Optional local synthetic smoke:

```bash
python - <<'PY'
# wrote synthetic SQL/schema files under /tmp/sqlrb_verieql_finite_bound_wrapper_mode_v0/
# called write_verieql_canary(..., verifier_mode="finite_bound", bound_size=10)
PY
```

## Validation Commands

```bash
find audits/verieql_finite_bound_wrapper_mode_v0 -name '*.md' -type f -size 0 -print
git diff --check
git status --short --untracked-files=all
git -C /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL status -sb
```
