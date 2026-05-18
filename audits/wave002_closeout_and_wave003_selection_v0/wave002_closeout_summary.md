# Wave 002 Closeout and Wave 003 Selection v0

## Purpose and Scope

This packet closes out the 28 policy-approved non-Common-core packages standardized in wave 002 and prepares a bounded wave 003 candidate queue. It is audit-only: no case packages were migrated or modified, no `case_sets/` files were changed, no denominators changed, no reports/results were written, no metrics were computed, and no paper tables were rendered.

## Wave 001 / Wave 002 Migration Progress

- Common-core canonical packages remain complete: 40/40.
- Wave 001 standardized non-Common-core packages: PORT_0002, PERF_0029.
- Wave 002 standardized non-Common-core packages: PERF_0002, CONS_0031, CONS_0034, PERF_0009, PERF_0010, PERF_0011, PERF_0012, PERF_0014, PERF_0015, PERF_0016, PERF_0018, PERF_0020, PERF_0021, PERF_0022, PERF_0023, PERF_0025, PERF_0026, PERF_0036, PERF_0038, PERF_0043, PERF_0044, PERF_0047, PERF_0050, PERF_0053, PERF_0063, PERF_0065, PERF_0066, PERF_0076.
- Current standardized non-Common-core package count: 30.
- Current release package count observed under `cases/*/*`: 70.

## Wave 002 Completed Package Review

The static review covered all 28 wave 002 packages. Each reviewed package has a release directory, public README, parsed manifest, parsed retained-evidence index, parsed provenance and denominator-eligibility metadata, parsed package-validation summary, source SQL, and positive SQL.

The package-validation summaries contain case-local claim boundaries and do not contain migration-task/global repository fields. README checks found no forbidden construction-process wording. Case-local `runs/README.md` boundary files are present, but raw legacy run payloads were not copied wholesale.

Review passed: yes.

## Recurring Issues

- The remaining universe still contains hygiene-risk rows with local-path/raw-log indicators, so wave 003 must reuse wave 002 archive-map and public-hygiene guardrails.
- Many remaining CONS and PERF rows have missing checker/core-asset flags and should stay backlog or manual-review rather than being selected for a high-throughput wave.
- Orphan or unregistered rows require registry/provenance reconciliation before any package standardization.

## Current Non-Common-core Standardization Count

- Known non-Common-core candidates from governance/preview: 157.
- Already standardized non-Common-core packages: 30.
- Remaining not-yet-standardized candidates: 127.

## Remaining Universe Summary

- Wave 003 auto candidates: 0.
- Wave 003 policy-approved candidates: 30.
- Wave 003 manual-review required: 13.
- Wave 003 backlog defer: 77.
- Orphan/unregistered review: 7.

## Recommended Wave 003 Scope

Attempt the 30 policy-approved candidates in `wave003_candidate_selection.csv`. These cases have complete source/positive/schema/checker core assets and match the wave-B hygiene profile that wave 002 policies already handled through archive mapping and fail-closed public-copy rules.

Recommended candidate ids: PERF_0027, PERF_0028, PERF_0030, PERF_0031, PERF_0032, PERF_0037, PERF_0039, PERF_0040, PERF_0041, PERF_0042, PERF_0045, PERF_0049, PERF_0051, PERF_0055, PERF_0057, PERF_0058, PERF_0059, PERF_0060, PERF_0061, PERF_0064, PERF_0067, PERF_0068, PERF_0069, PERF_0070, PERF_0071, PERF_0072, PERF_0073, PERF_0074, PERF_0075, PORT_0006.

Manual-review cases should remain excluded from wave 003 unless separately resolved: PERF_0001, PERF_0003, PERF_0004, PERF_0005, PERF_0046, PERF_0048, CONS_0001, CONS_0002, CONS_0003, CONS_0004, PORT_0001, LONGTAIL_0001, LONGTAIL_0002.

Backlog-defer examples: PERF_0078, PERF_0080, PERF_0081, PERF_0083, PERF_0084, PERF_0085, PERF_0086, PERF_0090, PERF_0091, PERF_0093, PERF_0094, PERF_0095, PERF_0096, PERF_0097, PERF_0101, PERF_0102, PERF_0103, PERF_0104, PERF_0105, PERF_0106 ....

Orphan/unregistered review cases should not be migrated until registry reconciliation: PERF_0079, PERF_0087, PERF_0092, PERF_0100, PORT_0007, LONGTAIL_0006, LONGTAIL_0017.

## Exact Next Safe Action

Run a separately authorized `overnight_non_common_core_case_package_standardization_wave_003` task using `audits/wave002_closeout_and_wave003_selection_v0/wave003_candidate_selection.csv`, migrating only `wave_003_policy_approved_candidate` rows and keeping `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged.
