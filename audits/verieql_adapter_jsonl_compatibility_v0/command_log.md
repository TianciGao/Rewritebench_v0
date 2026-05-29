# Command Log

## Preflight

```bash
git status -sb
rg -n "## D034|## D035" project_control/DECISION_LOG.md
test -f src/sql_rewrite_bench/verifier_support/verieql.py
test -d audits/local_verieql_raw_directory_probe_v0
test -d audits/legacy_baseline_smoke_verifier_clue_audit_v0
test -d /home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
git -C /home/tianci_gao/code/sql-rewrite-bench status --porcelain | wc -l
```

Result: release repo clean; D034/D035 present; required files/directories present; legacy dirty count was `1280`.

## Required Reads

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -n 90 project_control/MIGRATION_STATUS.md
tail -n 140 project_control/MIGRATION_RUN_LOG.md
sed -n '900,1075p' project_control/DECISION_LOG.md
sed -n '1,260p' repository_spec/verifier_support_output_contract_v0_draft.md
sed -n '1,240p' audits/local_verieql_raw_directory_probe_v0/README.md
sed -n '1,220p' audits/legacy_baseline_smoke_verifier_clue_audit_v0/README.md
sed -n '1,220p' audits/verieql_bounded_canary_v2/README.md
sed -n '1,360p' src/sql_rewrite_bench/verifier_support/verieql.py
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/verdicts.py
sed -n '1,260p' src/sql_rewrite_bench/verifier_support/summary.py
```

Result: completed.

## Validation

```bash
PYTHONPATH=src pytest tests/user_entry/test_verieql_support.py -q
PYTHONPATH=src pytest tests/user_entry/test_verifier_support.py tests/user_entry/test_verieql_support.py tests/user_entry/test_cli_facade.py -q
python -m py_compile src/sql_rewrite_bench/verifier_support/verieql.py src/sql_rewrite_bench/verifier_support/verdicts.py src/sql_rewrite_bench/verifier_support/summary.py src/cli/main.py
PYTHONPATH=src pytest tests/user_entry -q
```

Results:

- `13 passed` for focused VeriEQL tests.
- `40 passed` for focused verifier/CLI tests.
- `py_compile` passed.
- `211 passed, 1 skipped, 12 subtests passed` for full `tests/user_entry`.

## Dry-Run Smoke

Ran a temp-root dry-run JSONL construction smoke against the staged VeriEQL root. No verifier command was executed and no repository-level `output/` artifact was created.

Result:

```json
{"invocation_mode": "jsonl_batch", "jsonl_input_exists": true, "na_reason": "verieql_dry_run_not_executed", "semantic_equivalence_rate": null, "tool_available": true}
```

## Final Validation

```bash
git diff --check
python - <<'PY'
from pathlib import Path
import csv, json
root = Path('audits/verieql_adapter_jsonl_compatibility_v0')
for path in sorted(root.glob('*.md')):
    assert path.read_text(encoding='utf-8').strip(), f'empty markdown: {path}'
for path in sorted(root.glob('*.csv')):
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    assert rows and rows[0], f'empty csv: {path}'
for path in sorted(root.glob('*.json')):
    json.loads(path.read_text(encoding='utf-8'))
print('audit markdown/csv/json sanity ok')
PY
tail -n 3 project_control/MIGRATION_STATUS.md >/dev/null
tail -n 20 project_control/MIGRATION_RUN_LOG.md >/dev/null
git status --porcelain | awk '{print $2}' | grep -E '^(cases/|case_sets/|baselines/|reports/|results/|output/|benchmarks/|runs/user/)' || true
git status --porcelain | awk '{print $2}' | grep -E '^(output/|runs/user/)' || true
git -C /home/tianci_gao/code/sql-rewrite-bench status --porcelain | wc -l
```

Results:

- `git diff --check`: passed.
- Audit Markdown/CSV/JSON sanity: passed.
- Project-control readability: passed.
- Protected-surface check: no protected release-repo case/case_set/baseline/reports/results/output/benchmarks/runs paths reported.
- Runtime output check: no `output/` or `runs/user/` artifacts staged.
- Legacy repo dirty count remained `1280`, matching pre-existing state.
