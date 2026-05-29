# Command Log

## Release-Repo Preflight

```bash
git status -sb
rg -n "## D034|## D035" project_control/DECISION_LOG.md
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -f src/sql_rewrite_bench/verifier_support/sqlsolver.py
PYTHONPATH=src python -m cli.main user --help
test -d audits/legacy_verifier_tool_availability_audit_v0
test -d audits/local_verieql_raw_directory_probe_v0
test -d audits/verifier_support_fail_closed_closeout_v0
```

Result: passed. Release repo was clean before edits.

## Required Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 80 project_control/MIGRATION_STATUS.md
tail -n 120 project_control/MIGRATION_RUN_LOG.md
sed -n '923,1065p' project_control/DECISION_LOG.md
sed -n '1,220p' repository_spec/verifier_support_output_contract_v0_draft.md
sed -n '1,180p' audits/legacy_verifier_tool_availability_audit_v0/README.md
sed -n '1,180p' audits/local_verieql_raw_directory_probe_v0/README.md
sed -n '1,180p' audits/verifier_support_fail_closed_closeout_v0/README.md
sed -n '1,220p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '1,220p' src/sql_rewrite_bench/verifier_support/sqlsolver.py
```

Result: completed.

## Legacy Read-Only Inventory

```bash
pwd
git status -sb
git branch --show-current
git log --oneline -5
find reports/baseline_smoke -maxdepth 2 -type f | sort
grep -RIl --exclude-dir=.git -iE 'sqlsolver|verieql|support_readiness|equivalence|smt|solver|verifier' reports/baseline_smoke scripts src docs cases 2>/dev/null | head -200
grep -RIn --exclude-dir=.git -iE 'sqlsolver_verieql_support_readiness|baseline-smoke-sqlsolver-verieql-readiness|CONS_0007|support_candidate|schema_constraint_extraction|subset_policy|timeout_policy' . 2>/dev/null | head -300
```

Result: legacy repo was dirty before the audit; no writes were performed.

## Legacy File Inspection

```bash
python -m json.tool reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json | sed -n '1,240p'
python -m json.tool reports/baseline_smoke/sqlsolver_verieql_support_readiness_execute_refused_v0.json | sed -n '1,240p'
jq -r '.records[] | [.case_id,.pool,.recommended_status,.sqlsolver_support_risk,.verieql_support_risk,.support_usefulness,.reason] | @tsv' reports/baseline_smoke/sqlsolver_verieql_support_readiness_v0.json
sed -n '780,850p' scripts/cli.py
sed -n '1280,1348p' scripts/cli.py
sed -n '11560,11790p' scripts/cli.py
sed -n '49010,49035p' scripts/cli.py
sed -n '1,140p' docs/_scratch/SQLSOLVER_VERIEQL_SUPPORT_READINESS_AUDIT_v0.md
sed -n '1,130p' docs/_scratch/SQLSOLVER_ADAPTER_PREFLIGHT_CONS_0007_0035_v1.md
sed -n '1,125p' docs/_scratch/SQLSOLVER_RUNNER_DRY_RUN_WITH_JAR_CONS_0007_0035_v1.md
sed -n '1,130p' docs/_scratch/SQLSOLVER_SUPPORT_SMOKE_CONS_0007_0035_v1.md
sed -n '1,135p' docs/_scratch/SQLSOLVER_SUPPORT_SMOKE_ROLLUP_v1.md
sed -n '1,145p' docs/_scratch/VERIEQL_SUPPORT_BOOTSTRAP_PROBE_v0.md
sed -n '1,140p' docs/_scratch/VERIEQL_SUPPORT_WRAPPER_SCAFFOLD_v0.md
sed -n '1,145p' docs/_scratch/VERIEQL_SUPPORT_DEPENDENCY_PROBE_v0.md
sed -n '1,145p' docs/_scratch/VERIEQL_SUPPORT_CANARY_v0.md
sed -n '1,160p' docs/_scratch/VERIEQL_SUPPORT_VERDICT_INTERPRETATION_v0.md
sed -n '1,160p' docs/_scratch/PRIOR_SUPPORT_EVIDENCE_SUMMARY_SQLSOLVER_VERIEQL_v1.md
find reports/formal_expansion/verieql_support -maxdepth 2 -type f | sort
sed -n '1,4p' reports/formal_expansion/verieql_support/cons_0007_pairs.jsonl
sed -n '1,4p' reports/formal_expansion/verieql_support/cons_0035_pairs.jsonl
sed -n '1,4p' reports/formal_expansion/verieql_support/cons_0007_verieql_output.jsonl
sed -n '1,4p' reports/formal_expansion/verieql_support/cons_0035_verieql_output.jsonl
sed -n '1,4p' reports/formal_expansion/verieql_support/cons_0035_verieql_constraint_output.jsonl
```

Result: completed read-only. No real tools were run.

## Validation

```bash
git diff --check
git diff --name-only
find audits/legacy_baseline_smoke_verifier_clue_audit_v0 -type f | sort | xargs -r wc -l
python - <<'PY'
from pathlib import Path
import csv
root = Path('audits/legacy_baseline_smoke_verifier_clue_audit_v0')
for path in sorted(root.glob('*.md')):
    assert path.read_text(encoding='utf-8').strip(), f'empty markdown: {path}'
for path in sorted(root.glob('*.csv')):
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    assert rows and rows[0], f'empty csv: {path}'
print('audit markdown/csv sanity ok')
PY
git status --porcelain | awk '{print $2}' | grep -E '^(src/|tests/|scripts/|cases/|case_sets/|schemas/|inventory/|baselines/|reports/|results/|output/|benchmarks/|runs/user/)' || true
git -C /home/tianci_gao/code/sql-rewrite-bench status --porcelain | wc -l
```

Results:

- `git diff --check`: passed.
- Audit Markdown/CSV sanity: passed.
- Protected-surface check: no protected release-repo paths reported.
- Legacy repo dirty count remained `1280` after read-only inspection.
- No `runs/user/` or `output/` runtime artifacts were staged.
