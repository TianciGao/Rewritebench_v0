# Retained Evidence To Ledger Mapping Audit

Date: 2026-05-16

## Purpose And Scope

This audit maps the already-discovered Common-core v0 retained evidence candidates to the draft evidence ledger schema in `repository_spec/evidence_ledger_schema_v1_draft.md`.

The primary inputs are:

- `audits/reports_results_retained_evidence_map/retained_evidence_candidate_map.csv`
- `audits/reports_results_retained_evidence_map/reports_results_artifact_inventory.csv`
- `case_sets/common_core_v0/`
- `inventory/case_registry.csv`
- the redevelopment draft specs under `repository_spec/`

This task did not compute metrics. It did not copy reports/results. It did not implement adapters, scripts, a unified reproduction CLI, a user runner, or a paper table renderer. It did not update denominator values, case membership, paper results, or raw legacy evidence.

## Common-core Membership Basis

The mapping is bounded to fixed Common-core v0:

- 40 canonical case packages.
- Pool split: PERF 16, CONS 9, PORT 9, LONGTAIL 6.
- Track A same-engine scaffold: 120 planned rows.
- Control scaffold: 360 planned source/positive/hard-negative rows.

The aligned case-set and inventory files provide lookup context only. This audit does not change `case_sets/` or `inventory/`.

## Candidate Coverage Summary

The retained evidence candidate map contains 3,439 candidate rows:

- `method_output_retained_reference`: 3,080 rows.
- `paper_facing_retained_evidence`: 276 rows.
- `paper_summary_table`: 69 rows.
- `denominator_or_membership_reference`: 14 rows.

All candidate rows remain `copy_now=false`. Most rows need a future adapter and manual review before becoming ledger rows.

The artifact inventory also records report workspace groups that are not ledger inputs by default:

- local run workspaces: 4,885 artifacts.
- raw log/debug outputs: 4,094 artifacts.
- timing raw or timing log artifacts: 522 artifacts.
- unknown/manual-review artifacts: 233 artifacts.

These groups are reference/archive material unless a later curated migration selects public-safe summaries.

## Well-covered Ledger Fields

The following fields are well-covered by the candidate map or aligned release scaffolds:

- `case_set`
- `evidence_source`
- `retained_artifact_path`
- `notes`
- `method_role`

These fields can usually be populated from candidate metadata or constant Common-core v0 context.

## Missing Or Ambiguous Ledger Fields

Several fields need adapters or review before reliable ledger population:

- `case_id` and `pool` are direct for case-scoped candidates but ambiguous for mixed or PORT-wide candidates.
- `denominator_id` requires joining legacy denominator scope to `case_sets/common_core_v0/denominator_same_engine_120.csv`.
- `engine` is often not explicit in retained report artifact names and must be parsed or inferred from artifact contents.
- `route` and `method_role` require normalization from method strings such as `r_bot;portability` or `calcite_hep;portability`.
- `candidate_id` requires stable adapter-generated identifiers.
- `source_sql_path` and `candidate_sql_path` require joining candidate rows to canonical case packages and retained output locations.
- `executed`, `exact`, `result_status`, `checker_status`, `plan_available`, and `plan_artifact_path` require artifact-specific parsers.
- `parse_status`, `failure_stage`, `failure_type`, `timed`, `latency_ms`, and `speedup` are low coverage or metric-dependent from the current candidate map alone.

## Metric-dependent Fields

The following fields must not be interpreted as metric results until the metrics contract is finalized:

- `exact`
- `timed`
- `latency_ms`
- `speedup`
- `timing_eligible`
- derived performance distribution fields
- fallback/regression categories
- parseability/extractability/runnable SQL statuses

The retained evidence may contain raw material for these fields, but this audit does not compute or approve metric definitions.

## Recommended Adapter Design

Future adapters should be layered:

1. Load Common-core membership and denominator scaffolds from `case_sets/common_core_v0/`.
2. Load canonical case metadata from `inventory/case_registry.csv` and case manifests.
3. Read retained candidate maps and artifact inventories as source manifests.
4. Dispatch artifact-specific parsers for paper freeze ledgers, method outputs, hard-negative records, plan observability records, timing records, and paper summary indexes.
5. Emit draft ledger rows with explicit `available`, `unavailable`, `ambiguous`, `requires_adapter`, `requires_manual_review`, or `pending_metric_definition` states where values are not directly known.
6. Keep raw local run workspaces and raw logs private/archive-only unless separately curated.

## Recommended Next Safe Action

Review and approve the evidence ledger field semantics and adapter row-grain policy before implementing retained evidence adapters. Do not implement metrics computation, a paper table renderer, a unified reproduction CLI, or public runner outputs until final metric definitions and output policy are confirmed.
