# Normalization Gap Analysis

## What The Current Checker Normalizes

`src/sql_rewrite_bench/local_result_checker.py` reads source and candidate JSONL artifacts as lists of JSON objects. It then applies a small local normalization pass controlled by line-scanned keys in `checker/normalization.yaml`:

- `trim_whitespace`: strips leading and trailing whitespace from string values.
- `normalize_numeric_format`: parses string values with `Decimal` and writes a normalized decimal string.
- `sort_rows`: sorts normalized row dictionaries by their JSON representation.

After that pass, it compares the two lists of dictionaries with exact Python equality. It writes normalized JSONL artifacts and, on mismatch, a short `mismatch_summary.json` preview.

## What It Does Not Normalize

The current checker does not normalize or ignore output column labels. Dictionary keys must match exactly, so MySQL expression labels and PostgreSQL unlabeled-expression output such as `?column?` compare as different even when the single value is the same.

It does not implement several legacy normalization keys present in these PORT configs, including `normalize_decimal_strings`, `trim_trailing_whitespace`, and `row_order_sensitive`. `numeric_tolerance` is recognized as a known key for logging purposes, but the current comparison does not apply tolerance arithmetic.

It also does not provide cross-dialect coercion for date/time textual representations, boolean representations, null markers, or explicit multiset semantics beyond optional full-row sorting. It does not consume `compare_config.yaml` as an executable comparison policy; that file is currently required for presence only by the local checker path.

## Gaps That Matter Here

The controlled PORT run exposes two concrete cross-dialect gaps:

- Column-label gap: `PORT_0004`, `PORT_0013`, `PORT_0022`, and `PORT_0024` all compare one unnamed or expression-named scalar output against another. Values match by position, but keys differ.
- Decimal-string gap: `PORT_0022` and `PORT_0024` additionally differ by numeric rendering only. Decimal comparison shows equal values, but the configured legacy key is not implemented by the current checker.

No inspected mismatch required date/time, boolean, null, row-order, or multiset normalization to explain the observed artifacts.

## Future Policy Need

A future checker change should add explicit opt-in cross-dialect result normalization. The policy should be declared, tested, and narrow. It should not silently change same-engine checker behavior, and it should not treat `pos_01.sql` as a source oracle.

## Audit Boundary

No checker behavior was changed in this audit. The purpose was classification only, using local diagnostic artifacts from `runs/user/port_pg_target_reference_controlled/` and case-local checker configs.
