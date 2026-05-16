# CONS Hard-Negative Expected-Rejection Approval Sweep

Date: 2026-05-16

## Purpose and Scope

This is a read-only semantic review and approval-preparation audit for CONS Common-core v0 cases. It does not migrate cases, copy case packages, regenerate evidence, run DB validation, change denominator membership, or modify raw legacy evidence.

Reviewed cases: CONS_0005, CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012, CONS_0024, CONS_0036, CONS_0037.

CONS_0005 is included as an already migrated and maintainer-approved reference pattern only. The primary approval targets are CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012, CONS_0024, CONS_0036, CONS_0037.

## Current Boundary Statements

- Actual case migration performed: no.
- Common-core 40 blind/bulk migration started: no.
- Denominator changed: no.
- Paper results changed: no.
- Case membership changed: no.
- Raw legacy evidence changed: no.
- Legacy repository modified: no.

## Project-Control Staleness Note

The current `MIGRATION_STATUS.md` contains an older readiness-audit line recommending the first PERF batch (`PERF_0007`, `PERF_0008`, `PERF_0013`) even though later committed status blocks and audit outputs show the PERF wave-2 final batch completed. This audit records the discrepancy as historical/stale status text and only appends the current CONS approval sweep status; it does not rewrite history.

## Approval Status

- Approved reference: CONS_0005.
- Non-pilot cases reviewed: 8.
- High-confidence static inference requiring maintainer approval: 8.
- Cases ready for migration after approval: CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012, CONS_0024, CONS_0036, CONS_0037.
- Cases requiring defer before approval: none identified from this read-only review.

## Semantic Categories Found

- Correlated subquery predicate boundary: CONS_0007, CONS_0009, CONS_0010, CONS_0012.
- Outer join / NULL-preservation: CONS_0011, CONS_0024.
- Aggregation and group predicate boundary: CONS_0036.
- Duplicate multiplicity / DISTINCT aggregate semantics: CONS_0037.

## Recommended Next CONS Migration Batch

Primary recommendation: migrate CONS_0007, CONS_0009, CONS_0010, and CONS_0011 after maintainer approval of the expected rejection wording in this audit.

Fallback recommendation: migrate CONS_0007, CONS_0009, and CONS_0010 first if the maintainer wants a smaller initial CONS batch.

Do not migrate all eight remaining CONS cases at once. The semantic evidence is strong, but checker-heavy CONS migrations should stay small enough to isolate hard-negative wording, Spark plan sanitization, and validation-script caveats.

## Risks and Caveats

- All eight non-pilot cases still require maintainer approval before their future `checker/expected_rejections.yaml` entries should be marked approved.
- Spark plan text files and Spark validation scripts include expected local temporary path patterns and should be sanitized or mapped archive-only during actual migration.
- Several `tmp`/debug hygiene hits are false positives from SQL table names such as `tmp_emps` or plan text vocabulary; future public hygiene scans should classify by pattern category, not blindly by substring.
- This review uses static SQL differences and retained output evidence only; no DB rerun was performed.
