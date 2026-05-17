# candidate_status_parser_v0 Input Manifest Report

## Purpose And Scope

This report records manifest-first input selection for the bounded non-timing candidate status parser.
The manifest builder inspects release-repo locator and mapping metadata only. It does not open legacy files or parse retained evidence.

## Manifest Result

- Manifest rows: 0
- Approved parser inputs: 0
- Rejected/deferred metadata candidates: 9865
- Legacy files opened: false
- Production retained evidence parsed: false
- Metrics computed: false

Because no exact `case_id x engine x rewrite_method x candidate_id x denominator_id` source was verified from metadata, the manifest is header-only and the parser must fail closed.

## Metadata Sources Inspected

- `audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv`: rows=13190, method_related=8538, row_grain_verified=0, deferred=8538, methods=calcite_hep_fail_closed,direct_llm_original,direct_llm_repair_1,sqlglot_noop,sqlglot_optimize
- `audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv`: rows=3439, method_related=1323, row_grain_verified=0, deferred=1323, methods=calcite_hep_fail_closed,direct_llm_original,direct_llm_repair_1,sqlglot_noop,sqlglot_optimize
- `audits/retained_evidence_ledger_mapping/retained_evidence_to_ledger_field_map.csv`: rows=14, method_related=3, row_grain_verified=0, deferred=3, methods=calcite_hep_fail_closed,direct_llm_original,sqlglot_noop,sqlglot_optimize
- `audits/retained_evidence_ledger_mapping/common_core_ledger_source_inventory.csv`: rows=8, method_related=1, row_grain_verified=0, deferred=1, methods=calcite_hep_fail_closed,direct_llm_original,sqlglot_optimize

## Checks

- manifest file created: PASS (candidate_status_parser_input_manifest.csv written)
- manifest has header: PASS (columns=25)
- approved parser inputs = 0: PASS (approved_parser_inputs=0)
- legacy files opened = false: PASS (manifest builder reads release metadata only)
- production retained evidence parsed = false: PASS (no retained artifact content parsed)
- timing inputs approved = false: PASS (timing stays separate)
- prompt/token inputs approved = false: PASS (prompt/token risky inputs are not approved)
- raw log inputs approved = false: PASS (raw log inputs are not approved)
- header-only fail-closed manifest when no row-grain sources: PASS (no exact row-grain metadata source was approved)

## Non-goals

- No parser implementation is run by this script.
- No row statuses are filled.
- No timing fields are approved.
- No metric input is authorized.
- No metrics are computed.
- No reports/results, denominator, paper-result, case membership, or raw legacy evidence changes are made.

## Next Safe Action

Run `parse_candidate_status_from_manifest.py`. With the current header-only manifest, the expected safe behavior is a 600-row unresolved ledger with `parser_status=no_approved_row_level_inputs`.
