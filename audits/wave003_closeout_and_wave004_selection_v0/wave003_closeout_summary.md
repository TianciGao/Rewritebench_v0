# Wave 003 Closeout And Wave 004 Selection

## Purpose And Scope

This closeout reviews the 30 non-Common-core case packages standardized in wave 003 and builds a wave 004 selection queue from the remaining governed non-Common-core universe. No new case packages were migrated, no case package contents were changed, no `case_sets/` files were modified, no denominators changed, no reports/results were written, no metrics were computed, and no paper tables were rendered.

## Wave 001 / Wave 002 / Wave 003 Progress

- Wave 001 completed cases: 2.
- Wave 002 completed cases: 28.
- Wave 003 completed cases reviewed here: 30.
- Standardized non-Common-core packages from wave audits: 60.
- Current release package count from `cases/*/*`: 100.
- Current non-Common-core release package count from `cases/*/*` minus Common-core membership: 60.

## Wave 003 Completed Package Review

All 30 wave 003 packages exist under `cases/<POOL>/<CASE_ID>/` and were reviewed statically. README template checks, manifest YAML parsing, package-validation summary schema checks, runs-retention presence, provenance metadata, denominator eligibility metadata, source SQL, positive SQL, claim-boundary checks, and public hygiene checks passed for all reviewed cases.

Completed wave 003 cases: PERF_0027, PERF_0028, PERF_0030, PERF_0031, PERF_0032, PERF_0037, PERF_0039, PERF_0040, PERF_0041, PERF_0042, PERF_0045, PERF_0049, PERF_0051, PERF_0055, PERF_0057, PERF_0058, PERF_0059, PERF_0060, PERF_0061, PERF_0064, PERF_0067, PERF_0068, PERF_0069, PERF_0070, PERF_0071, PERF_0072, PERF_0073, PERF_0074, PERF_0075, PORT_0006.

## Validation Summary

- Static package review rows: 30.
- Review passed: yes.
- JSON/YAML parse: passed for reviewed package metadata and audit summary outputs.
- Fixture smoke: pending final command run in this task's validation phase.
- `git diff --check`: pending final command run after project-control writeback.

## Recurring Issues

The remaining governed universe is no longer dominated by simple wave-B archive-map cases. The remaining 97 candidates require either manual review, missing checker/core asset resolution, or registry reconciliation. Under the current wave 002/003 policies, there are no safe auto or policy-approved wave 004 migration candidates.

## Current Non-Common-Core Standardized Count

The recomputed standardized non-Common-core count is 60. This matches the wave-audit total of 60 completed non-Common-core packages.

## Remaining Universe Summary

- Known non-Common-core planning rows: 157.
- Remaining not-yet-standardized or orphan/unregistered rows: 97.
- Wave 004 auto candidates: 0.
- Wave 004 policy-approved candidates: 0.
- Wave 004 manual-review rows: 13.
- Wave 004 backlog-defer rows: 77.
- Orphan/unregistered review rows: 7.

## Recommended Wave 004 Scope

Do not run package migration wave 004 yet. First run a manual/policy resolution packet focused on missing checker/core package assets, hard-negative/checker approval, and orphan/registry reconciliation. A future wave 004 migration prompt should execute only if that packet produces nonzero `wave_004_auto_migration_candidate` or `wave_004_policy_approved_candidate` rows.

## Exact Next Safe Action

Prepare a separately authorized wave 004 blocker-resolution packet for the 13 manual-review rows, 77 missing-checker backlog rows, and 7 orphan/unregistered rows without migrating cases, changing `case_sets/`, changing denominators, updating reports/results, changing paper results, computing metrics, rendering paper tables, or modifying raw legacy evidence.
