# Common-core 40 v2 Conversion Plan Command Log

- Repository preflight: confirmed `/home/tianci_gao/code/Rewritebench_v0`, branch `feature/case-package-v2-external-schema`, remote `origin`, and clean starting status.
- Read project-control files.
- Read Common-core metadata from `case_sets/common_core_v0/cases.csv`, `denominator_same_engine_120.csv`, `controls_360.csv`, and `inventory/case_registry.csv`.
- Read accepted pilot and evidence-removal parity outputs.
- Read v2 rulebook folder-order artifacts.
- Inspected current tracked top-level assets for all 40 Common-core case packages without modifying case files.
- Confirmed 40 Common-core cases reviewed.
- Confirmed five accepted pilots: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.
- Classified 35 non-pilot cases into Wave A, Wave B, Wave C/manual, and blocked manual-review buckets.
- Drafted Common-core 40 readiness, folder-order, schema-grouping, evidence-policy, conversion-wave, and manual-review blocker outputs.
- No DB/checker execution, official metric computation, reports/results migration, denominator update, case-set update, inventory update, or leaderboard output was performed.
- Ran summary JSON assertion: passed.
- Ran CSV parse/header checks for required CSV outputs: passed.
- Ran protected-boundary diff check for `cases/`, `schemas/`, `evidence/`, `case_sets/`, `inventory/`, `reports/`, and `results/`: no changes.
- Ran `git diff --check`: passed.
- Ran `git status -sb`: reviewed changed paths before explicit staging.
