# Candidate Status Whitelist Triage Summary

## Purpose and Scope

This audit prepares a small maintainer-reviewable whitelist proposal for a future `candidate_status_parser_v1`.

Scope is limited to the five Track-A same-engine rewrite candidate routes already present in the 600-row scaffold:

- `direct_llm_original`
- `direct_llm_repair_1`
- `sqlglot_optimize`
- `sqlglot_noop`
- `calcite_hep_fail_closed`

The audit considered only non-timing candidate status fields: `generated`, `ready`, `executed`, `exact`, `result_status`, `failure_stage`, `failure_type`, `parse_status`, `checker_status`, `retained_artifact_path`, and `evidence_source`.

No candidate statuses were parsed or filled. No timing fields were filled. No metrics were computed. No production ledger was created.

## Why Parser v0 Had 0 Approved Inputs

`candidate_status_parser_v0` required exact row-grain proof at `case_id x engine x rewrite_method x candidate_id x denominator_id`. The release-repo locator and mapping metadata did not prove any source at that grain, so the v0 input manifest was header-only:

- approved inputs: 0
- row-level statuses filled: 0
- unresolved rows: 600

This was the correct fail-closed behavior. Route-level summaries and metric tables were not distributed into candidate rows.

## Candidate Selection Method

The triage reviewed release-repo metadata and selected legacy inventory paths only at path, size, extension, and header/schema-preview level. It prioritized files whose names or headers suggested row-level status metadata for the five in-scope routes.

Likely useful sources were those with identifiers such as `case_id`, `engine`, `route_id`, `method_id`, `denominator_id`, `row_key`, `execution_status`, `exact_match`, `generation_status`, `failure_stage`, or `failure_type`.

Sources were rejected or deferred when they were aggregate-only, timing/performance-bearing, prompt/token adjacent, raw-log adjacent, local-path-hygiene risky, or missing exact row-grain proof.

Files reviewed at metadata/header level: 28.

## Proposed Approvals

The proposal contains 19 maintainer-reviewable rows:

- `approve_header_only_then_parser`: 4
- `defer_manual_review`: 6
- `reject_route_level_only`: 3
- `reject_timing_or_performance`: 5
- `retain_reference_only`: 1

The original triage did not approve any parser input by itself; approval status is recorded separately in the maintainer decision sheet.

## Maintainer Approval Recorded

On 2026-05-17, the maintainer approved `candidate_status_parser_v1` use of these proposal IDs only:

- `P001`
- `P002`
- `P003`
- `P011`
- `P012`

The approved scope is limited to the approved non-timing fields and required conditions recorded in `candidate_status_manual_decision_sheet.csv`. Timing fields, metric fields, metric input authorization, production ledger promotion, reports/results updates, denominator changes, paper-result changes, and raw legacy evidence mutation remain out of scope.

All other proposal rows are not approved for parser-v1 use by this approval record unless a later maintainer decision explicitly changes that status.

## Rejected or Deferred Groups

Rejected groups include aggregate method cards, proposed paper rows, validity summaries, run-result summaries, timing/performance event logs, and route-level summaries. These cannot be used by a non-timing row-level parser without a separate sanitized projection or separate timing/metrics authorization.

Deferred groups include files that may contain row-level status evidence but need maintainer approval for header-only probing, column projection, route identity, denominator derivation, or public-hygiene constraints.

## Manual Decisions Needed

Maintainer review is needed to decide whether any `approve_header_only_then_parser` or `defer_manual_review` row may become an approved v1 manifest input.

Approval should specify:

- exact source path or path pattern
- allowed parser fields
- forbidden columns
- required row keys
- whether denominator and candidate ID derivation are allowed
- public-hygiene conditions for path-like columns

## Boundaries

This triage did not modify the legacy repo, copy reports/results, create `results/retained`, create `reports/evaluation`, change denominators, change case membership, change paper results, parse candidate statuses, parse timing files, fill timing fields, or compute metrics.

## Exact Next Safe Action

Implement `candidate_status_parser_v1` from the five maintainer-approved whitelist entries only, with non-timing fields only, `metric_input_authorized=false`, no metrics, and fail-closed row-grain validation.
