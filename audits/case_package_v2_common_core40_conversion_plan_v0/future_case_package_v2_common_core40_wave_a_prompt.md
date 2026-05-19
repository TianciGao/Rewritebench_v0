# Future Prompt: case_package_v2_common_core40_wave_a_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify main.
- Do not inspect or modify the legacy repo.

Task title:
`case_package_v2_common_core40_wave_a_v0`

This is a branch-only writable Wave A conversion task.

This task converts only these Common-core Wave A cases:

- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`

This is NOT full Common-core 40 conversion.
This is NOT PORT conversion.
This is NOT DB/checker execution.
This is NOT official metric computation.
This is NOT reports/results migration.
This is NOT denominator update.
This is NOT case_sets update.
This is NOT global leaderboard creation.

Goal:
Convert the five Wave A TPC-H cases to the accepted clean-template-minimal v2 target using the pilot pattern.

Required read inputs:
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_conversion_plan_summary.md`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_case_readiness.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_v2_folder_order_plan.csv`
- `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_schema_grouping_plan.csv`
- Accepted pilot case packages and prior v2 policy outputs

Folder order:
`manifest -> sql -> schema -> checker -> validation -> witness -> evidence_policy -> metadata -> notes -> runs -> README/validator`

Expected high-level actions:
- Create direct `sql/pos_01.sql` and `sql/neg_01.sql` paths.
- Create or verify external `schemas/tpch_common_core40_v0/` before deleting case-local schema engine directories.
- Use profile-first `schema_ref`.
- Keep checker as YAML configuration only.
- Replace old engine validation scripts with thin wrappers only after wrapper reference checks.
- Use source-as-oracle witness policy.
- Replace static evidence refs with regeneration-first `evidence_policy`.
- Remove metadata/data/notes/static evidence only after live references are updated and validator passes.
- Do not recreate case-local `runs/`.

Hard boundaries:
- Do not modify cases outside the five Wave A cases.
- Do not modify `case_sets/`.
- Do not modify inventory.
- Do not modify reports/results.
- Do not change denominators or paper results.
- Do not compute official metrics.
- Do not run DB/checker execution.
- Do not create leaderboard output.
- Do not use `git add .`.

Validation:
- Run static v2 validator for all five Wave A cases.
- Run `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Run JSON and protected-boundary checks.
- Run `git diff --check`.

Exact next action after Wave A:
Run a read-only Wave A parity review before authorizing Wave B.
