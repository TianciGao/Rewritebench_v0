# Manifest Caveat Closeout v0

## Purpose and scope

This branch-only task reviewed the retained manual-review provenance caveats from `case_package_v2_manifest_contract_repair_v0` for the 32 already converted v2 cases. It did not perform Wave C conversion, new case conversion, DB/checker execution, official metric computation, reports/results migration, denominator updates, case-set updates, inventory updates, or leaderboard creation.

Target cases reviewed: 32 converted v2 cases covering accepted pilots, Wave A, and Wave B.

## Why closeout was needed

The manifest semantic-contract repair restored taxonomy, source/provenance/status/caveat fields, and validator support for all 32 converted v2 cases, but retained 19 explicit provenance caveat rows across 17 cases. Those caveats needed classification so Wave C planning is not blocked by non-substantive draft-origin fallback caveats, while unrecovered source-path facts remain explicit.

## Caveat classification summary

- Caveats reviewed: 19.
- Draft-origin caveats accepted as non-blocking: 17.
- Safe field-level repairs applied: 1 (`PORT_0003` `draft_origin.origin_id` now uses the branch-history `source_entry_pointer` fallback instead of the literal `manual_review_required` placeholder).
- Remaining manual-review caveats: 2 (`PERF_0077` and `PERF_0082` `source_path`).
- No taxonomy, source identity, benchmark identity, or draft origin was invented.

## Safely repaired fields

`PORT_0003` branch-history provenance records `source_entry_pointer: datasets/raw/parrot/PARROT/benchmark/BIRD/pg_res.json[3]`. Because the manifest already marks `draft_origin.origin_type` as `source_query_identity_fallback`, the placeholder `draft_origin.origin_id: manual_review_required` was safely replaced with that source-entry pointer without claiming a distinct draft artifact.

## Accepted non-blocking caveats

The 17 draft-origin caveats were retained in manifests as `draft_origin_not_explicitly_recovered_nonblocking`. These cases have source-family, source-query/source-entry identity, source path where recovered, taxonomy, clean v2 physical paths, and static validator pass status. The caveat now means only that a separate explicit draft artifact was not recovered and is not being fabricated.

## Remaining manual-review caveats

`PERF_0077` and `PERF_0082` still have `source_path: manual_review_required`. Branch-history provenance records `source_entry: ''` and `source_materialization: legacy case-local source.sql` for both, so the original JOB/IMDB source path was not safely recoverable from allowed sources. These caveats do not block Wave C planning, but they should be resolved or explicitly accepted before public source-path closeout.

## Wave C readiness implication

Wave C planning is allowed after this closeout because the remaining manual-review rows are not Wave C cases and do not affect converted-case clean-template validity. A narrow source-path provenance follow-up remains advisable before final public release or any claim that all 32 converted manifests have fully recovered source paths.

## Protected boundary summary

No case-set, inventory, reports/results, denominator, paper-result, official-metric, DB/checker execution, or leaderboard surfaces were changed. No deleted compatibility directories or `evidence/cases/` surfaces were restored.

## Exact next safe action

Authorize `case_package_v2_common_core40_wave_c_manual_review_plan_v0` for remaining PORT/manual-review Common-core planning, while keeping a separate narrow `PERF_0077`/`PERF_0082` source-path provenance follow-up before final public release if exact JOB source locators are required.
