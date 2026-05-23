# Implementation Summary

## Code Changes

Updated:

- `src/sql_rewrite_bench/verifier_support/verieql.py`
- `tests/user_entry/test_verieql_support.py`

The wrapper now has two invocation modes:

1. `direct_command`
   - Preserves the existing simple command behavior used by synthetic tests.
   - Invokes a command as `command source.sql comparison.sql`.

2. `jsonl_batch`
   - Enabled when `SQLRB_VERIEQL_ROOT` or `VERIEQL_ROOT` points to a staged VeriEQL source tree.
   - Validates root shape by checking for `parallel/cli_within_timeout.py`.
   - Builds JSONL input and invokes module-mode batch CLI from the VeriEQL root.

## New Public Helper Functions

- `write_verieql_pair_jsonl`
- `build_verieql_jsonl_record`
- `build_verieql_batch_command`
- `parse_verieql_output_file`
- `normalize_verieql_jsonl_record`

These helpers are intentionally small and local-diagnostic scoped.

## Output Behavior

The wrapper still writes only under:

```text
output/results/<run_id>/verifier/
output/logs/<run_id>/verifier.log
output/reports/<run_id>/verifier_summary.md
```

For JSONL batch mode, the generated batch artifacts are placed under:

```text
output/results/<run_id>/verifier/tools/verieql/batch/
  verieql_pairs.jsonl
  verieql_output.jsonl
  raw_stdout.txt
  raw_stderr.txt
```

Per-pair raw files remain under:

```text
output/results/<run_id>/verifier/tools/verieql/<pair_id>/
```

## Compatibility Boundary

The implementation does not install VeriEQL dependencies. If the staged source root is present but imports fail, the wrapper records a local `tool_error` and sets summary `na_reason=verieql_dependency_missing`.
