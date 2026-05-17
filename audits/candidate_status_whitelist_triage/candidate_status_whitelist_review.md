# Candidate Status Whitelist Review Guide

## Review Scope

This review guide is for maintainer triage only. It does not approve parser inputs by itself.

The proposed sources are grouped by recommended decision in `candidate_status_whitelist_proposal.csv`. All parser manifest preview rows remain `pending_maintainer_review`.

## Approve Header Only Then Parser

These files look most likely to support a bounded non-timing parser after maintainer approval.

`P003` `direct_llm_execute_repair_1shot_01/repair_failures.csv`

- Might support: `failure_stage`, `failure_type`, `result_status`, `retained_artifact_path`, `evidence_source`.
- Remaining risk: denominator and candidate ID are not explicit and would need deterministic derivation from scaffold route context.
- Maintainer decision needed: approve or reject denominator/candidate derivation for repair failures.

`P011` `calcite_hep_120_post93_frontier_audit_v1.csv`

- Might support: `result_status`, `failure_stage`, `failure_type`, `retained_artifact_path`, `evidence_source`.
- Remaining risk: `row_key` mapping and retained path hygiene need review.
- Maintainer decision needed: approve or reject row-key to candidate-row mapping.

`P012` `calcite_hep_120_recovery_round3c_numeric_scale_canary_02_01/run_event_long.csv`

- Might support: `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `checker_status`, `retained_artifact_path`.
- Remaining risk: only covers a bounded subset and must not imply status for unmatched scaffold rows.
- Maintainer decision needed: approve subset parsing while leaving unmatched rows unresolved.

`P013` `calcite_hep_120_recovery_round3c_numeric_scale_canary_02_01/metadata/LONGTAIL_0013/mysql/row_metadata.json`

- Might support: `executed`, `exact`, `result_status`, `checker_status`, `retained_artifact_path`.
- Remaining risk: single-row JSON pattern and local DB metadata must be excluded from parser output.
- Maintainer decision needed: approve a constrained `row_metadata.json` pattern or reject until a cleaner projection exists.

## Defer Manual Review

These files may contain useful information but need a stricter decision before parser use.

- `P001` direct LLM generation matrix: row-like generation data but prompt/path hygiene risks.
- `P002` direct LLM repair candidate set: row-like original and repair status data but includes timing-bearing and source-artifact columns.
- `P006` SQLGlot case matrix: case-level preflight data without explicit per-engine candidate row grain.
- `P007` SQLGlot non-port method summary: method/case summary lacks explicit engine and candidate ID.
- `P008` SQLGlot resolved PORT method summary: route scope may be mixed or not same-engine-only.
- `P014` Calcite recovery priority: row key may encode the case but `case_id` is not explicit.

## Reject or Reference Only

Reject parser use for route-level summaries, paper cards, proposed method rows, aggregate validity tables, and timing/performance-bearing run results. These may remain documentation or reference metadata but must not be converted into row statuses.

`P018` is a release-repo source inventory row and should remain locator metadata only.

## Maintainer Questions

- Which proposed sources may be opened beyond header/schema preview?
- Which columns are explicitly allowed for parser v1?
- Is denominator or candidate ID derivation from scaffold context allowed for any source?
- Should timing-bearing sources be rejected outright or projected into sanitized non-timing views by a separate task?
- Should path-like fields be retained as evidence pointers or stripped for public hygiene?

## Next Safe Action

Fill `candidate_status_manual_decision_sheet.csv`. Only rows explicitly approved there should be converted into a future `candidate_status_parser_v1` manifest.
