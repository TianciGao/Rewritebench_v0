# Command Log

Initial checks:

```bash
git status -sb
git branch --show-current
git log --oneline -12
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

Context read included project-control files, recent PORT/MySQL audits, current runner/execution/checker modules, the existing PostgreSQL target-reference adapter, and the four target PORT manifests.

Controlled reverse diagnostic:

```bash
cat > /tmp/sqlrb_port_reverse_cross_dialect_cases.txt <<'EOF'
PORT_0003
PORT_0005
PORT_0008
PORT_0012
EOF
PYTHONPATH=src python -m sql_rewrite_bench.user_run   --case-set common_core_v0   --engine mysql   --case-list /tmp/sqlrb_port_reverse_cross_dialect_cases.txt   --adapter-command "python examples/user/port_mysql_target_reference_adapter.py"   --out runs/user/port_mysql_target_reference_controlled   --enable-db-execution   --enable-checker
```

Regression and validation:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run   --case-set common_core_v0   --engine postgres   --case-list /tmp/sqlrb_port_forward_cross_dialect_cases.txt   --adapter-command "python examples/user/port_postgres_target_reference_adapter.py"   --out runs/user/port_forward_regression_after_reverse   --enable-db-execution   --enable-checker
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/port_reverse_public_smoke_capture
git diff --check
PYTHONPATH=src python -m py_compile examples/user/port_mysql_target_reference_adapter.py src/sql_rewrite_bench/engine_execution.py
PYTHONPATH=src pytest tests/user_entry
PYTHONPATH=src python -m unittest discover -s tests/user_entry -p 'test_*.py'
PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -p 'test_*.py'
PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <each Common-core case path>
```

`pytest` was unavailable in this local environment, so the equivalent unittest suite was used and passed.

Local run outputs are not committed.
