# Current Behavior

## Label Comparison

`local_result_checker.py` reads source and candidate result artifacts as JSONL rows where each row must be a JSON object. Engine result exporters use result-column labels as JSON object keys.

The same-engine comparison path:

1. reads JSONL rows into `list[dict[str, object]]`;
2. normalizes values through `_normalize_rows`;
3. preserves object keys during value normalization;
4. compares the complete row lists with `normalized_source == normalized_candidate`.

Because Python dictionary equality includes key equality, column labels are compared as part of exactness. This is implicit through JSONL structure, not an explicit named policy.

## Config Surface

The current checker requires:

- `checker/checker.yaml`
- `checker/normalization.yaml`
- `checker/compare_config.yaml`

For same-engine rows, the checker currently consumes only a small set of normalization settings such as:

- `trim_whitespace`
- `normalize_numeric_format`
- `sort_rows`

The inspected checker configs do not define a same-engine label policy such as `compare_column_labels` or `label_policy`.

## Cross-dialect Exception

`user_run.py` enables cross-dialect checker normalization only when resolved manifest metadata says:

- `diagnostic_mode == cross_dialect_reference`
- `checker.comparison == source_reference_result_to_target_candidate_result`

In that opt-in path, `_cross_dialect_compare` compares row counts, column counts, and positional values. It records `positional_column_comparison_used: true`.

That behavior is role-gated cross-dialect normalization, not a global rule for same-engine rows.

## Status Surface

Current checker outputs distinguish:

- checker success;
- checker mismatch;
- checker failed/missing config;
- exact versus mismatch.

They do not separately report:

- `value_exact`;
- `label_exact`;
- `label_only_mismatch`;
- explicit-alias mismatch versus generated-expression label mismatch.

The five inspected MySQL rows therefore appear as generic `checker_mismatch` / `mismatch`, even though their values match positionally.
