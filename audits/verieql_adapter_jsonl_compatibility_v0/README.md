# verieql_adapter_jsonl_compatibility_v0

## Verdict

Implementation verdict: `jsonl_compatibility_layer_implemented_fail_closed_local_only`.

The VeriEQL wrapper now supports a staged VeriEQL source root via `SQLRB_VERIEQL_ROOT`, emits VeriEQL-style JSONL pair input, constructs the batch CLI command shape, parses VeriEQL JSONL output records, and keeps missing-root/missing-dependency behavior fail-closed.

No dependencies were installed. The staged VeriEQL source tree was not modified, copied, or vendorized. No real Common-core or CONS canary was run. No official Semantic Equivalence Rate, official metrics, retained evidence, top-level reports/results, or leaderboard output was produced.

## Implementation Summary

- Updated `src/sql_rewrite_bench/verifier_support/verieql.py`.
- Preserved the prior direct-command synthetic/fake-command path.
- Added `SQLRB_VERIEQL_ROOT` and `VERIEQL_ROOT` detection for JSONL batch mode.
- Added JSONL pair file generation under the local D035 verifier output area.
- Added batch command construction for:

```text
python -m parallel.cli_within_timeout -f <pairs.jsonl> -t <timeout> -o <output.jsonl>
```

- Added parser/normalizer support for VeriEQL output JSONL records with `states`, `err`, and `counterexample` fields.
- Added dry-run support for JSONL and command construction without invoking VeriEQL.
- Added dependency-missing fail-closed handling for `ModuleNotFoundError` / missing import failures.

## Validation Summary

- Focused VeriEQL tests: `13 passed`.
- Focused verifier/CLI tests: `40 passed`.
- Full `tests/user_entry`: `211 passed, 1 skipped, 12 subtests passed`.
- `py_compile`: passed.
- Temp-root JSONL dry-run smoke against the staged root: passed.

## Boundary

This is compatibility infrastructure only. It does not make VeriEQL available, does not install missing packages, and does not convert historical support evidence into release-repo official evidence.
