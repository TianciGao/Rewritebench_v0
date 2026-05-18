# Wave 004 Blocker Resolution Packet v0

## Purpose And Scope

This packet reviews the remaining non-Common-core case universe after wave 003 closeout and decides whether any remaining rows can be batch-unlocked for a later wave 004 migration task. It does not migrate cases, create case-set membership, change denominators, update reports/results, compute metrics, render paper tables, or modify raw legacy evidence.

## Current Remaining Universe State

- Known non-Common-core candidates from wave 003 closeout: 157.
- Standardized non-Common-core packages after waves 001-003: 60.
- Remaining rows reviewed in this packet: 97.
- Current wave 004 buckets reviewed: 13 manual-review, 77 backlog-defer, and 7 orphan/unregistered.
- New case migrations performed: no.

## Blocker Categories

Primary blocker counts from the wave004 candidate selection are:

- Missing checker or checker package-core blocker: 78 rows.
- Schema/load gap with checker/manual package-core blocker: 6 rows.
- Hard-negative or checker semantic approval needed with otherwise core-complete rows: 6 rows.
- Orphan/unregistered registry reconciliation needed: 7 rows.

Cross-cutting preview risk flags remain visible:

- Local-path or public-hygiene risk: 86 rows.
- Raw-log/debug/trace risk: 84 rows.
- Legacy runs mapping unclear or missing: 18 rows.
- Schema/load gap flag: 6 rows.
- Missing-checker flag: 84 rows.
- Registry/orphan flag: 7 rows.

## Policy Questions Reviewed

Seven policy questions were reviewed: missing checker, missing retained evidence, hard-negative review, schema/load gaps, orphan/unregistered registry reconciliation, public hygiene, and minimal package policy.

The recommended decisions are fail-closed:

- Do not relax the source.sql and positive.sql requirement.
- Do not batch-create packages with no checker package assets.
- Keep `evidence_not_retained` available only when source/positive/checker/package core is complete.
- Keep static-inferred hard negatives as manual-review items unless explicitly approved by a human.
- Require registry reconciliation before orphan/unregistered package standardization.
- Archive-map or exclude local-path/raw-log/prompt/token/API artifacts; do not copy them.
- Require README template v1, package_validation_summary schema v1, provenance, denominator boundary metadata, and explicit no-leaderboard/no-paper/no-metric claims for any future package.

## Recommended Wave004 Candidate Unlocks

This packet recommends zero immediate wave004 policy-approved candidates.

- Policy-unlocked candidates: 0.
- Manual-review cases retained: 13.
- Backlog-defer cases retained: 77.
- Orphan/registry review cases retained: 7.

## Cases That Must Remain Manual, Backlog, Or Orphan

- Manual-review rows require human checker/schema/hard-negative review before they can become package-migration candidates.
- Backlog-defer rows are dominated by missing checker or incomplete package-core assets and should not be migrated under the current canonical-package guardrails.
- Orphan/unregistered rows require a separate registry reconciliation preview before any public package standardization.

## Exact Next Safe Action

Prepare a manual checker/schema/hard-negative and orphan registry reconciliation packet before any wave004 migration; do not migrate cases until source/positive/checker core assets and registry identity are resolved.
