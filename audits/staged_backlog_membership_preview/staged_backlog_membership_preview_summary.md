# Staged/Backlog Membership Preview

Date: 2026-05-17

## Purpose And Scope

This preview organizes the 157 non-Common-core legacy case-like directories into human-reviewable staged/backlog planning groups. It uses the completed case-universe governance audit and overnight investigation bundle as inputs.

No official `case_sets/staged_v0` or `case_sets/backlog_v0` files were created. No cases were migrated. No `case_sets/common_core_v0/`, inventory, reports, results, denominator values, paper results, metrics, scripts, runner interfaces, or raw legacy evidence were changed.

## Fixed Common-core v0 Boundary

Common-core v0 remains exactly 40 canonical case packages with Track A 120 planned same-engine rows. Non-Common-core cases in this preview are not public v0 main-denominator rows and must not be treated as Common-core members.

## Counts By Proposed Membership Status

| Proposed status | Count |
|---|---:|
| `proposed_staged_v0` | 61 |
| `proposed_backlog_v0` | 76 |
| `manual_review_required` | 13 |
| `orphan_or_unregistered_review` | 7 |
| `duplicate_or_alias_review` | 0 |
| `exclude_private_or_scratch` | 0 |
| `defer_post_release` | 0 |

## Pool Split By Proposed Status

| Pool | Proposed status | Count |
|---|---|---:|
| CONS | `manual_review_required` | 4 |
| CONS | `proposed_backlog_v0` | 19 |
| CONS | `proposed_staged_v0` | 8 |
| LONGTAIL | `manual_review_required` | 2 |
| LONGTAIL | `orphan_or_unregistered_review` | 2 |
| LONGTAIL | `proposed_backlog_v0` | 14 |
| PERF | `manual_review_required` | 6 |
| PERF | `orphan_or_unregistered_review` | 4 |
| PERF | `proposed_backlog_v0` | 43 |
| PERF | `proposed_staged_v0` | 36 |
| PORT | `manual_review_required` | 1 |
| PORT | `orphan_or_unregistered_review` | 1 |
| PORT | `proposed_staged_v0` | 17 |


## Staged Versus Backlog

`proposed_staged_v0` means the case appears plausible for a later staged release preview after bounded maintainer review, evidence indexing, and hygiene checks. It is still not part of Common-core v0 and does not change the denominator.

`proposed_backlog_v0` means the case remains governed as a plausible future case but is not staged-ready. These cases commonly need retained-evidence indexing, checker/hard-negative review, local-path/log hygiene planning, or canonical migration planning before they can be considered staged.

## Treatment Of The Seven Unregistered Directories

The seven detected but unregistered directories are forced into `orphan_or_unregistered_review` in this preview:

- `LONGTAIL_0006`: `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `LONGTAIL_0017`: `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0079`: `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0087`: `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: local_absolute_path, WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0092`: `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PERF_0100`: `register_later_as_backlog`; checker directory absent; runs/evidence absent; no retained execution evidence located; hygiene terms found: WSL, stdout; manifest explicitly says registry not updated/not registered
- `PORT_0007`: `staged_review_candidate`; checker directory absent; PORT_0007 has validation/checker.yaml only; runs/evidence absent; no retained execution evidence located; manifest explicitly says registry not updated/not registered


These directories must be reconciled against the legacy registry before any staged/backlog membership decision. This task does not register or exclude them.

## Manual-review Summary

Manual-review and orphan rows are collected in `manual_review_and_orphan_cases.csv`. They include cases with missing skeleton assets, explicit human-review flags, unregistered status, or other review blockers. Counts:

- `manual_review_required`: 13
- `orphan_or_unregistered_review`: 7
- `duplicate_or_alias_review`: 0
- `exclude_private_or_scratch`: 0
- `defer_post_release`: 0

## Risks And Caveats

- Planning labels are not official membership.
- Non-Common-core cases cannot enter the Common-core denominator without a separate governance decision, which is not authorized here.
- Many legacy cases have local-path/log hygiene or missing-checker risk inherited from legacy `runs/` and case-local files.
- Unregistered directories require registry reconciliation before public release classification.
- Future migration still requires bounded case-package migration tasks and validator checks.

## Recommended Next Action

Review this preview, decide whether the staged/backlog criteria are acceptable, then run a separate official membership-file planning task if approved. Do not migrate cases, create official staged/backlog case sets, change denominators, update reports/results, or implement metrics/runners/adapters yet.

## What Must Not Be Done Yet

Do not create official `case_sets/staged_v0/` or `case_sets/backlog_v0/` files, migrate non-Common-core cases, copy raw retained runs/logs, compute metrics, render paper tables, change Common-core membership, or update denominator values based on this preview alone.
