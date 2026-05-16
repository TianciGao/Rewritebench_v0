# Common-core Case-Package Migration Status Closeout

Date: 2026-05-16

## Purpose And Boundary

This closeout verifies the current Common-core v0 case-package migration state from release-repo files and validator v0.3 outputs. It did not migrate cases, copy evidence, run DB engines, regenerate evidence, update case sets, update reports/results, change denominators, or change paper results.

Fixed Common-core v0 denominator remains 40 cases: 16 PERF, 9 CONS, 9 PORT, and 6 LONGTAIL. Track A remains 120 planned same-engine rows.

Common-core 40 blind/bulk migration was not started; this snapshot only records bounded case-package migration state.

## Current Pool Completion

| Pool | Canonical complete | Common-core total | Status |
|---|---:|---:|---|
| PERF | 16 | 16 | complete at canonical case-package level |
| CONS | 9 | 9 | complete at canonical case-package level |
| PORT | 9 | 9 | complete at canonical case-package level; `PORT_0004` now passes canonical-case after upgrade |
| LONGTAIL | 1 | 6 | only `LONGTAIL_0011` complete; five cases remain |
| Total | 35 | 40 | Common-core case-package migration is not complete |

## Canonical-Complete Cases

PERF: PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0034, PERF_0035, PERF_0052, PERF_0054, PERF_0056, PERF_0062, PERF_0077, PERF_0082.

CONS: CONS_0005, CONS_0007, CONS_0009, CONS_0010, CONS_0011, CONS_0012, CONS_0024, CONS_0036, CONS_0037.

PORT: PORT_0003, PORT_0004, PORT_0005, PORT_0008, PORT_0012, PORT_0013, PORT_0022, PORT_0024, PORT_0025.

LONGTAIL: `LONGTAIL_0011`.

## Remaining Cases

The remaining not-yet-canonical Common-core cases are `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024`. They are not present as release case directories in this snapshot and remain in the readiness audit's complex LONGTAIL/structure-review wave.

## Validator Summary

- Full-case validator v0.3: PASS 35/35 over the expected canonical-complete set.
- Canonical-case validator v0.3: PASS 35/35 over the same set.
- Canonical warnings: `PORT_0004` and `PORT_0008` use the accepted transitional PostgreSQL validation alias `validation/run_pg_validation.sh`.
- The five remaining LONGTAIL cases were intentionally excluded from validator runs because they have not yet been migrated.

## Major Remaining Blockers

- The five remaining LONGTAIL cases need structural boundary and hard-negative review before migration.
- Validation scripts in migrated packages are retained legacy assets, not final public user runners.
- A reports/results retained evidence map has not been completed.
- Script inventory and final public runner output policy remain pending.
- Case universe 197 vs 190 governance reconciliation remains pending.

## Explicit Non-Changes

- `case_sets/` was not updated.
- `reports/` and `results/` were not updated.
- The Common-core denominator was not changed.
- Paper results were not changed.
- Common-core membership was not changed.
- Raw legacy evidence was not changed.
- No global leaderboard or new benchmark claim was created.

## Recommended Next Safe Action

Review this closeout, then plan the remaining LONGTAIL bounded wave. LONGTAIL final wave planning can be the next safe task. Do not touch `case_sets/`, `reports/`, `results/`, denominator files, or paper tables yet. A bounded LONGTAIL migration should follow only after review.
