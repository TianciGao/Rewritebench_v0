# Test Results

## Focused VeriEQL Compatibility Tests

```bash
PYTHONPATH=src pytest tests/user_entry/test_verieql_support.py -q
```

Result:

```text
13 passed in 0.13s
```

## Focused Verifier / CLI Tests

```bash
PYTHONPATH=src pytest tests/user_entry/test_verifier_support.py tests/user_entry/test_verieql_support.py tests/user_entry/test_cli_facade.py -q
```

Result:

```text
40 passed in 0.18s
```

## Py Compile

```bash
python -m py_compile src/sql_rewrite_bench/verifier_support/verieql.py src/sql_rewrite_bench/verifier_support/verdicts.py src/sql_rewrite_bench/verifier_support/summary.py src/cli/main.py
```

Result: passed.

## Dry-Run JSONL Smoke

Used staged root:

```text
/home/tianci_gao/code/sql-rewrite-bench/datasets/raw/verieql/staged/VeriEQL
```

Ran temp-output dry-run only. Result:

```json
{
  "invocation_mode": "jsonl_batch",
  "jsonl_input_exists": true,
  "na_reason": "verieql_dry_run_not_executed",
  "semantic_equivalence_rate": null,
  "tool_available": true
}
```

## Full User-Entry Tests

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result:

```text
211 passed, 1 skipped, 12 subtests passed in 3.97s
```
