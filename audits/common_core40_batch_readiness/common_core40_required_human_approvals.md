# Common-core 40 Required Human Approvals

This file lists items requiring human decisions before future migration. It does not approve migration.

## Checker Expected Rejection Reason

- CONS non-pilots: `CONS_0007`, `CONS_0009`, `CONS_0010`, `CONS_0011`, `CONS_0012`, `CONS_0024`, `CONS_0036`, `CONS_0037`. Need maintainer-approved semantic reason for each hard negative.
- LONGTAIL non-pilots: `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, `LONGTAIL_0024`. Need structural/hard-negative boundary approval where applicable.
- PORT manual-review/defer cases: `PORT_0022`, `PORT_0024`, `PORT_0025`. Need approval for evidence boundary and hard-negative/publication handling.

## Public Hygiene / Sanitization Policy

- Sanitized Spark plan policy exists, but each future batch must confirm sanitized copies preserve plan evidence and remove local path traces.

## Archive-Only Evidence

- Raw logs and non-public-safe run artifacts require archive-only or summary mapping. No deletion is authorized.

## Ambiguous Hard-Negative N/A

- If any future detailed inspection finds a missing or engine-N/A hard negative, stop and get case-specific approval before manifesting the boundary.

## Performance / Timing Boundary

- PERF batches require explicit no-new-speedup/no-new-timing-claim statements. Human review is required if timing artifacts are proposed for public evidence.

## Workload-Frequency Boundary

- LONGTAIL batches require explicit no-workload-frequency/no-production-frequency statements.

## Defer / Manual Review

- Defer until reviewed: `PORT_0022`, `PORT_0024`, `PORT_0025`.
