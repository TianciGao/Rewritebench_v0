# Case Universe Governance Summary

Date: 2026-05-17

## Purpose And Scope

This read-only governance audit indexes the whole legacy case universe after Common-core 40 canonical migration completed. It explains the detected legacy case-like directories, reconciles the 197 detected directories against the prior 190 registered-package context, classifies non-Common-core cases into future release-readiness buckets, and prepares post-release planning prompts.

No case migration occurred. No non-Common-core package was copied into the release repository. No `case_sets/`, `reports/`, `results/`, denominator values, paper results, case membership, scripts, metrics, adapters, DB validation, timing, or raw legacy evidence were changed.

## Fixed Common-core v0 Boundary

Common-core v0 remains exactly 40 cases: PERF 16, CONS 9, PORT 9, and LONGTAIL 6. These 40 cases are already canonical in the public release repo and remain the only public v0 main denominator. Non-Common-core cases are governed backlog/universe material and are not part of the v0 denominator.

## Detected Universe

- Total detected case-like directories under legacy `cases/<POOL>/`: 197.
- Prior legacy registry rows: 190.
- Registered cases physically present: 190.
- Detected but not registered: 7.
- Registered but not detected: 0.

## Counts By Pool

| Item | Count |
|---|---:|
| CONS | 40 |
| LONGTAIL | 24 |
| PERF | 105 |
| PORT | 28 |

## Counts By Bucket

| Item | Count |
|---|---:|
| backlog_candidate | 76 |
| common_core_v0 | 40 |
| manual_review_required | 13 |
| orphan_or_unregistered | 7 |
| staged_candidate | 61 |

## Common-core 40 Status

All 40 fixed Common-core cases remain canonical-complete in the release repository. This audit did not revalidate or alter those packages.

## Non-Common-core Summary

There are 157 detected non-Common-core case-like directories. The main non-Common-core readiness buckets are:

| Item | Count |
|---|---:|
| backlog_candidate | 76 |
| manual_review_required | 13 |
| orphan_or_unregistered | 7 |
| staged_candidate | 61 |

## Main Risks

| Item | Count |
|---|---:|
| checker_missing | 112 |
| local_path_risk | 184 |
| prompt_api_token_risk | 0 |
| public_hygiene_risk | 184 |
| raw_log_debug_risk | 162 |
| runs_exists | 156 |
| schema_missing | 6 |

Key risk interpretation:

- Local path risk is common because legacy retained `runs/` and plan/log artifacts often contain local execution traces.
- Raw log/debug risk is common and should be handled by retention mapping or sanitized public summaries, not wholesale copying.
- Prompt/API/token risk was not detected by this static scan.
- Legacy `evidence/` directories are not present under detected case packages; retained evidence is mostly represented by `runs/`, validation assets, reports, and case-local files.

## Recommended Next Phase

Do not migrate non-Common-core cases yet. First run a staged/backlog membership planning task to decide which non-Common-core cases are release candidates, backlog candidates, manual-review items, or exclusions. Then plan low-risk post-release batches, starting with staged candidates that have complete core files and limited hygiene risk.
