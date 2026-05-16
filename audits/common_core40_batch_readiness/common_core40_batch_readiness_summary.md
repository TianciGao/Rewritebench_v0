# Common-core 40 Batch Migration Readiness Summary

Date: 2026-05-16
Mode: readiness audit and migration wave planning only; legacy repository read-only.

## Purpose and Scope

This audit inspects the fixed Common-core v0 membership of 40 cases and plans future migration waves. It does not move case files, copy case packages, regenerate evidence, run database engines, update case sets, change denominators, or change paper results.

Fixed benchmark facts preserved:

- Common-core v0 remains 40 cases.
- Pool split remains 16 PERF, 9 CONS, 9 PORT, and 6 LONGTAIL.
- Track A same-engine denominator remains 120 planned rows.
- Case package remains the benchmark unit.
- Reporting remains role-aware and denominator-aware.
- No global leaderboard is introduced.
- Raw legacy evidence is unchanged.

## Current Pilot Baseline

Completed representative full-case pilots:

- `PORT_0004`: legacy-compatible full-case pilot.
- `PORT_0008`: canonical-layout PORT pilot with sanitized retained evidence.
- `CONS_0005`: canonical-layout CONS checker/hard-negative pilot.
- `PERF_0006`: canonical-layout PERF analytical/performance-boundary pilot.
- `LONGTAIL_0011`: canonical-layout LONGTAIL structural-complexity pilot.

All four pools now have representative full-case pilots. Common-core 40 migration has not started.

## Legacy State Snapshot

- Branch: `artifact/case-package-contract-alignment-clean`
- HEAD: `7e438b5d767922007a1ca456fed0bf2e237a8952`
- Status summary: `## artifact/case-package-contract-alignment-clean...origin/artifact/case-package-contract-alignment-clean [behind 7]`
- Existing dirty legacy files were observed under reports/evaluation/common_core_v0; they were not modified.
- Last five commits inspected read-only:

```text
7e438b5d docs: rewrite README for common-core reproducibility
6eefb7c2 docs: rewrite README for common-core reproducibility
c1cc0ff1 artifacts: add common-core reproduction input bundle
6724042d artifacts: add common-core table reproduction provenance
e05032f7 cases: add provenance blocks to CONS manifests
```

## Counts by Wave

- `wave_0_already_piloted`: 5
- `wave_1_low_risk_direct_canonical`: 0
- `wave_2_sanitized_plan_needed`: 19
- `wave_3_checker_hard_negative_approval_needed`: 8
- `wave_4_complex_longtail_or_structure_review`: 5
- `wave_5_reports_results_dependency`: 0
- `wave_6_defer_manual_review`: 3

## Counts by Pool

- PERF: 16
- CONS: 9
- PORT: 9
- LONGTAIL: 6

## Major Blockers

- Spark plan/local-path traces require sanitized public plan copies and raw-original mapping before public publication.
- Checker-heavy CONS cases need maintainer-approved expected rejection reasons before migration.
- LONGTAIL cases need structural boundary review so realistic SQL shape is not overclaimed as workload-frequency evidence.
- PORT_0022, PORT_0024, and PORT_0025 retain log/raw evidence ambiguity and prompt/token-like risk and should not be batch-migrated blind.
- All Common-core cases are report/paper-freeze referenced, so migration must preserve paper-result and denominator boundaries.

## Recommended Next Batch

Primary next batch: `PERF_0007`, `PERF_0008`, `PERF_0013`.

Reason: these PERF cases match the completed `PERF_0006` pattern, exercise performance-boundary packaging, and require a small repeatable sanitized-plan workflow without new speedup or timing claims.

Fallback: `PERF_0007` only.

## What Not To Do Yet

- Do not migrate all remaining 35 cases at once.
- Do not start Common-core 40 migration without reviewing this wave plan.
- Do not copy raw `runs/` wholesale.
- Do not publish raw Spark plans with local-path traces.
- Do not create new speedup, workload-frequency, ranking, denominator, or paper-result claims.
- Do not update `case_sets/` in the readiness stage.

## Why Blind Batch Migration Is Unsafe

The 40 cases share a common case-package shape, but the retained evidence is not uniform: PORT has dialect and raw-plan hygiene pressure; CONS needs semantic checker approvals; PERF has speedup-overclaim risk; LONGTAIL has structural-overclaim risk. Validator v0.3 can verify canonical layout after migration, but it does not infer SQL semantics, approve hard-negative reasons, sanitize raw plans automatically, or certify paper-facing reports.

## Suggested Codex xhigh Autonomy Model

- Use medium autonomy for small sanitized-plan batches after explicit prompt approval.
- Use low autonomy for CONS and LONGTAIL because semantic approvals are case-specific.
- Use human-required mode for PORT_0022, PORT_0024, and PORT_0025 until raw logs and prompt/token-like findings are resolved.
