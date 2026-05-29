# Command Log

Preflight:

```bash
git status -sb
rg -n "D034|D035" project_control/DECISION_LOG.md
rg -n "D035|superseded|output/results|src/cli|benchmarks/" project_control/MIGRATION_MASTER_PLAN.md
test -d src/cli
test -f src/sql_rewrite_bench/user_output.py
test -d audits/user_cli_facade_phase2b_review_v0
```

Implementation review:

```bash
sed -n '1,420p' src/cli/main.py
sed -n '1,280p' tests/user_entry/test_cli_facade.py
rg -n "write_.*report|metrics_summary|verifier|failure_buckets|tag_slices|boundary|summary" src/sql_rewrite_bench/user_output.py
sed -n '220,390p' src/sql_rewrite_bench/user_output.py
```

Validation:

```bash
PYTHONPATH=src pytest tests/user_entry/test_cli_facade.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/cli/__init__.py src/cli/__main__.py src/cli/main.py
git diff --check
```

Temp-output smoke:

```bash
tmpdir="$(mktemp -d /tmp/sqlrb_phase2c_summary_XXXXXX)"
mkdir -p "$tmpdir/output/reports/demo" "$tmpdir/output/results/demo"
PYTHONPATH=src python -m cli.main user summarize --output-root "$tmpdir/output" --run-id demo
PYTHONPATH=src python -m cli.main user show-boundary --output-root "$tmpdir/output" --run-id demo
rm -rf "$tmpdir"
```
