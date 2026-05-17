# Candidate Status Whitelist Review Guide

## Review Scope

This review guide is for maintainer triage only. It does not approve parser inputs by itself.

The proposed sources are grouped by recommended decision in `candidate_status_whitelist_proposal.csv`. The parser manifest preview now marks only the five explicitly approved rows as `approved_by_maintainer`.

## Approval Update

On 2026-05-17, the maintainer approved `P001`, `P002`, `P003`, `P011`, and `P012` for `candidate_status_parser_v1` use under the approved fields and required conditions recorded in `candidate_status_manual_decision_sheet.csv`.

This approval does not authorize timing fields, metric fields, metric input authorization, metrics computation, production ledger promotion, reports/results updates, denominator changes, paper-result changes, or raw legacy evidence mutation.

## Approved For Parser V1

`P001` `direct_llm_preflight/direct_llm_generation_matrix.csv`

- Approved fields: `generated`, `ready`, `failure_stage`, `failure_type`, `evidence_source`.
- Conditions: parse only non-timing generation/status columns; do not read prompt payloads or generated SQL payloads; require exact row keys; leave ambiguous rows unresolved.

`P002` `00_PAPER_EVIDENCE_FREEZE_V1/direct_llm_execute_repair_candidate_set_v1.csv`

- Approved fields: `generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `retained_artifact_path`.
- Conditions: ignore `original_timing_success` and raw `source_artifacts`; parse only non-timing original/repair status columns; leave ambiguous rows unresolved.

`P003` `direct_llm_execute_repair_1shot_01/repair_failures.csv`

- Approved fields: `failure_stage`, `failure_type`, `result_status`, `retained_artifact_path`, `evidence_source`.
- Conditions: denominator and candidate ID may be derived from scaffold route context only when unique.

`P011` `calcite_hep_120_post93_frontier_audit_v1.csv`

- Approved fields: `result_status`, `failure_stage`, `failure_type`, `retained_artifact_path`, `evidence_source`.
- Conditions: `row_key` must map uniquely to candidate ID and denominator ID; public path hygiene must be enforced.

`P012` `calcite_hep_120_recovery_round3c_numeric_scale_canary_02_01/run_event_long.csv`

- Approved fields: `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `checker_status`, `retained_artifact_path`.
- Conditions: parse bounded subset rows only and leave unmatched scaffold rows unresolved.

## Previously Recommended Header-Only Candidates

These files looked most likely to support a bounded non-timing parser after maintainer approval.

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
- Maintainer decision needed: not approved in the explicit `P001`, `P002`, `P003`, `P011`, `P012` approval set; requires separate approval before parser use.

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

Use only the five explicitly approved rows in `candidate_status_manual_decision_sheet.csv` to implement a future `candidate_status_parser_v1` manifest. Do not include non-approved rows without a separate maintainer decision.
