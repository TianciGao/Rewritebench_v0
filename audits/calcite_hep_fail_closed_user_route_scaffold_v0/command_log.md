# Command Log

Preflight and inspection:

```bash
git status -sb
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor ae6a0c84bd57f1687c8201ce9fbd97c5b77dae97 origin/feature/case-package-v2-external-schema
rg -n "calcite|hep|heuristic|rule" src tests scripts docs repository_spec project_control pyproject.toml .github
python -m cli.main user list-cases --case-set common_core_v0 --engines postgres --smoke
python -m cli.main user explain-selection --case-set common_core_v0 --engines postgres --smoke
python -m cli.main user show-output-schema
python -m cli.main user show-boundary
python -m cli.main user evaluate --help
java -version
env | rg "^(SQLRB_CALCITE|CALCITE)"
```

Implementation validation:

```bash
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py tests/user_entry/test_local_metrics.py tests/user_entry/test_user_output.py -q
pytest tests/user_entry -q
python -m py_compile src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py src/sql_rewrite_bench/local_timing.py
git diff --check
git status -sb
```

Tiny smoke:

```bash
python - <<'PY'
# Selected CONS_0036, CONS_0037, PERF_0006 and invoked
# src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py through adapter_runner.
PY

python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --pool all \
  --engines postgres \
  --case-list /tmp/sqlrb_calcite_hep_fail_closed_user_route_scaffold_v0/case_list.txt \
  --adapter-command "python src/sql_rewrite_bench/calcite_hep_fail_closed_adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_fail_closed_user_route_scaffold_v0/d035_output \
  --run-id calcite_hep_scaffold_smoke \
  --adapter-timeout 10
```

The transient `runs/user/calcite_hep_scaffold_smoke` source-run directory created by the D035 export facade was removed after copying smoke evidence to `/tmp`.
