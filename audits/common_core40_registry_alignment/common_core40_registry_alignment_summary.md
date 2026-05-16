# Common-core 40 Registry Alignment Summary

Date: 2026-05-16

## Purpose And Scope

This task aligns the machine-readable release membership, denominator scaffold, and public inventory registries for Common-core v0 after canonical case-package migration completed 40/40. It did not migrate cases, run DB engines, regenerate evidence, rerun timing, update reports/results, update paper tables, change denominator values, change paper results, change case membership, or mutate raw legacy evidence.

## Created Or Updated

- `case_sets/common_core_v0/manifest.yaml`: release membership manifest for the fixed Common-core v0 set.
- `case_sets/common_core_v0/cases.csv`: 40 Common-core case membership rows.
- `case_sets/common_core_v0/denominator_same_engine_120.csv`: 120 planned Track A same-engine denominator scaffold rows.
- `case_sets/common_core_v0/controls_360.csv`: 360 planned source/positive/hard-negative control route scaffold rows.
- `inventory/case_registry.csv`: Common-core-only public v0 case registry with 40 rows.
- `inventory/source_registry.csv`: source-family registry inferred from existing migrated case manifests.

## Row Counts

| File | Data rows |
|---|---:|
| `case_sets/common_core_v0/cases.csv` | 40 |
| `case_sets/common_core_v0/denominator_same_engine_120.csv` | 120 |
| `case_sets/common_core_v0/controls_360.csv` | 360 |
| `inventory/case_registry.csv` | 40 |
| `inventory/source_registry.csv` | 8 |

## Fixed Denominator Reminder

Common-core v0 remains exactly 40 cases with pool split PERF 16, CONS 9, PORT 9, LONGTAIL 6. Track A remains 120 planned same-engine rows. The denominator scaffold is a planned membership scaffold only; it is not execution evidence, a result table, or a metric computation.

## Relation To Final Closeout

This alignment uses the final Common-core 40 closeout under `audits/common_core40_final_closeout/`, where validator v0.3 full-case and canonical-case both passed 40/40. No new validator semantics were introduced.

## Explicit Non-Changes

- Reports were not updated.
- Results were not updated.
- Paper tables were not updated.
- Denominator values were not changed.
- Paper results were not changed.
- Case membership was not changed.
- Raw legacy evidence was not changed.
- No global leaderboard or benchmark-result claim was created.

## Remaining Blockers

Reports/results retained evidence mapping, public runner/output policy, script inventory and reproduction path, whole-case universe governance reconciliation, and release tagging remain pending separate tasks.

## Recommended Next Phase

Proceed with the reports/results retained evidence map next, using the newly aligned `case_sets/common_core_v0/` and `inventory/` files as stable membership inputs. Keep paper tables, denominator values, and result metrics unchanged unless a separate task explicitly authorizes that scope.
