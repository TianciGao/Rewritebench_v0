# SQLGlot Status Projection And Dry-Run v4

## Commands

```bash
python scripts/dev/build_sqlglot_status_source_manifest.py \
  --triage audits/candidate_status_evidence_completion_round1/sqlglot_candidate_source_triage.csv \
  --decision-sheet audits/candidate_status_evidence_completion_round1/sqlglot_candidate_manual_decision_sheet.csv \
  --manifest-preview audits/candidate_status_evidence_completion_round1/sqlglot_parser_v1_manifest_preview.csv \
  --out-dir audits/sqlglot_status_projection_v1

python scripts/dev/build_sqlglot_non_timing_projection.py \
  --manifest audits/sqlglot_status_projection_v1/sqlglot_status_source_manifest.csv \
  --out-dir audits/sqlglot_status_projection_v1

python scripts/dev/parse_sqlglot_candidate_status_v1.py \
  --scaffold audits/rewrite_candidate_adapter_v0/rewrite_candidate_scaffold_ledger_v0.csv \
  --projection-index audits/sqlglot_status_projection_v1/sqlglot_non_timing_projection_index.csv \
  --out-dir audits/sqlglot_candidate_status_parser_v1

python scripts/dev/build_combined_candidate_status_overlay_v2.py \
  --base-candidate-ledger audits/candidate_status_parser_v1/candidate_status_parsed_ledger_v1.csv \
  --sqlglot-ledger audits/sqlglot_candidate_status_parser_v1/sqlglot_candidate_status_ledger_v1.csv \
  --combined-authorization audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv \
  --out-dir audits/combined_candidate_status_overlay_v2

python scripts/dev/compute_normalized_status_only_metrics_dryrun_v4.py \
  --combined-candidate-ledger audits/combined_candidate_status_overlay_v2/combined_candidate_status_ledger_v2.csv \
  --combined-authorization audits/overlap_priority_overlay_v1/combined_metric_input_authorization_overlay_v1.csv \
  --inference-overlay audits/status_inference_overlay_v0/status_inference_overlay_v0.csv \
  --denominator case_sets/common_core_v0/denominator_same_engine_120.csv \
  --out-dir audits/normalized_status_only_metrics_dryrun_v4
```

## Inputs

- Existing SQLGlot round1 triage, manual decision sheet, and manifest preview.
- Existing 600-row rewrite candidate scaffold.
- Existing candidate status parser v1 and overlap authorization outputs.
- SGL011 sanitized checker-event source only, read at non-timing status-column level.

## Projection Rules

- SGL011 is the only approved projection/parser source in v1.
- P006 remains pending because deterministic engine expansion is not explicitly approved.
- P009 is rejected for this bounded manifest because of mixed portability plus timing/path risk.
- SGL012 is held out as a duplicate of SGL011.
- SGL013 is rejected because raw stdout/stderr pointers and denominator joins remain unsafe.
- Timing, speedup, latency, prompt/token, raw-log, and artifact payload columns are not retained.

## Parser Rules

- Parser scope is limited to `sqlglot_optimize` and `sqlglot_noop`.
- Rows require case_id x engine x rewrite_method row grain after route mapping.
- Executed/exact/checker status can be filled from SGL011.
- Generated/ready are not inferred from checker artifact path presence.
- Unmatched SQLGlot scaffold rows remain unresolved.

## Dry-Run Rules

- v4 remains audit-only and preserves 600 planned candidate rows.
- SQLGlot projection rows are included only as bounded audit dry-run inputs.
- Official metric flags and paper-result flags remain false.
- Timing/performance metrics are not computed.

## Non-Goals

- No official metrics.
- No paper tables.
- No reports/results updates.
- No denominator or case-set changes.
- No timing adapter or performance computation.

## Warnings

- SQLGlot coverage is partial because SGL011 covers 137 of 240 SQLGlot scaffold rows.
- SQLGlot Generation Rate dry-run remains limited because generated/ready are not source-observed in SGL011.
- Future official metrics require a separate authorization and production-readiness review.
