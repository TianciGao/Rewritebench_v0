# Diagnostic Fields Schema

The new fields are local diagnostic metadata only. They do not alter strict checker exactness.

## CheckerResult.details

- `value_exact`: boolean. True when normalized values match positionally after existing normalization and row/column shape checks pass.
- `label_exact`: boolean. True when normalized result column labels match exactly under the strict current policy.
- `label_only_mismatch`: boolean. True only when values match positionally but labels differ, with row count and column count unchanged.
- `label_policy`: string. Currently `strict`.
- `label_mismatch_class`: string. Currently `none` or `unclassified_label_difference`.
- `value_mismatch_reason`: string. One of `none`, `row_count_mismatch`, `column_count_mismatch`, or `value_mismatch`.

## Mismatch Artifact

Mismatch artifacts now include a top-level `label_diagnostics` object with the same behavior-preserving fields.

## Quality Summary

`quality_summary.json` now includes:

```json
{
  "diagnostic_counts": {
    "label_only_mismatch_rows": 0
  }
}
```

The targeted rerun produced:

```json
{
  "diagnostic_counts": {
    "label_only_mismatch_rows": 5
  }
}
```

## Interpretation

`label_only_mismatch=true` means local diagnostic values are positionally exact but strict labels differ. It is not an exactness override. Rows with this marker still remain `checker_mismatch`, `exact_status=mismatch`, and `failure_bucket=mismatch`.
