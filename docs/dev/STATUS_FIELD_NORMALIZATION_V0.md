# STATUS_FIELD_NORMALIZATION_V0

## Command

```bash
python scripts/dev/normalize_candidate_status_fields.py \
  --candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --authorization-overlay audits/metric_input_authorization_overlay_v0/metric_input_authorization_overlay_v0.csv \
  --out-dir audits/status_field_normalization_v0
```

## Inputs

- `candidate_status_parsed_ledger_v1.csv`
- `metric_input_authorization_overlay_v0.csv`

## Outputs

Outputs are written only under `audits/status_field_normalization_v0/`.

## Normalized Fields

`generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `parse_status`, and `checker_status`.

## Non-Goals

No official metrics, paper tables, reports/results updates, timing fields, speedup fields, denominator changes, paper-result changes, overlap-row authorization, unresolved-row authorization, or legacy evidence parsing are performed.

## Manual Mapping Behavior

Unrecognized field/raw-value pairs are normalized to `needs_manual_mapping` and emitted in `status_normalization_manual_review_rows.csv`. Unknown evidence availability is preserved as `unknown`, not coerced to `false`.

## Next Step

Review the normalization overlay and observed-value inventory. A future status-only metrics dry-run v1 over normalized fields requires separate authorization.
