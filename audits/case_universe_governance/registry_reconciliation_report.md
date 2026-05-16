# Registry Reconciliation Report

Date: 2026-05-17

## Detected Count Versus Registered Context

The legacy `cases/` tree contains 197 case-like directories under the four governed pools. The legacy `inventory/case_registry.csv` contains 190 registered case rows.

All 190 registered case IDs are physically present in the legacy `cases/` tree. The count difference is caused by 7 detected case-like directories that are not present in the legacy registry.

## Detected But Not Registered

- `LONGTAIL_0006`
- `LONGTAIL_0017`
- `PERF_0079`
- `PERF_0087`
- `PERF_0092`
- `PERF_0100`
- `PORT_0007`

## Registered But Not Detected

None.

## Duplicate Or Alias Findings

No duplicate case IDs were detected in the legacy registry. Alias status is not asserted by this audit; the seven unregistered directories require registry review before they can be classified as true cases, aliases, scratch remnants, or exclusions.

## Reconciliation Needed Before Extended Release

Before any extended or staged release membership is created, the project should:

- decide whether each unregistered directory is a valid case, duplicate/alias, scratch artifact, or private exclusion;
- decide whether legacy registry rows with `not_assessed` or `staged_not_yet_admitted` should become staged release candidates or backlog only;
- confirm retained evidence and runs retention policy for each future batch;
- avoid changing Common-core v0 membership or denominator values.

## v0 Denominator Boundary

Non-Common-core cases are not part of the public v0 main denominator. Common-core v0 remains 40 cases and Track A remains 120 planned same-engine rows.
