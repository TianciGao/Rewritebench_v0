# Non-PORT Regression Protection

## Protected Pools

The PORT role metadata design must not change behavior for:

- PERF
- CONS
- LONGTAIL

Same-engine local diagnostic behavior remains the default for cases without explicit cross-dialect metadata.

## Representative Regression Cases

Future P2/P3 validation should include:

- `PERF_0006`
- `CONS_0005`
- `LONGTAIL_0011`

Required checks:

- case selection still reads from `case_sets/common_core_v0/`;
- no `cases/` scanning is used for membership;
- no denominator files are modified;
- existing smoke dry-run behavior is unchanged;
- existing smoke adapter-capture behavior is unchanged;
- existing quality report generation is unchanged;
- existing tag slice generation is unchanged;
- PostgreSQL same-engine diagnostics remain unchanged for non-PORT cases.

## Manifest Metadata Boundary

Future P2 should patch only the 9 Common-core PORT manifests if authorized. It must not add cross-dialect metadata to PERF, CONS, or LONGTAIL as part of the PORT task.

## Fail-Closed Behavior

If a non-PORT case lacks `local_diagnostic`, the runner should use current same-engine behavior. It should not fail solely because the new PORT metadata block is absent.

## Prohibited Regressions

- No source SQL edits.
- No case membership changes.
- No denominator changes.
- No reports/results updates.
- No official metrics.
- No timing/speedup.
- No tag score/ranking.
- No leaderboard.
