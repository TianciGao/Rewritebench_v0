# Future Prompt: case_package_v2_common_core40_wave_b_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Task title: `case_package_v2_common_core40_wave_b_v0`

This is a bounded writable Common-core Wave B v2 conversion task. Convert only the schema-grouped non-PORT Wave B cases identified in `audits/case_package_v2_common_core40_conversion_plan_v0/common_core40_conversion_waves.csv`.

Use the accepted clean-template-minimal pilot cases and the completed Wave A cases as canonical examples. Follow folder order:

`manifest -> sql -> schema -> checker -> validation -> witness -> evidence_policy -> metadata -> notes -> runs -> README/validator`

Hard boundaries:
- Do not convert Wave C or D008-blocked PORT cases.
- Do not modify `case_sets/`, inventory, reports, results, denominators, paper results, official metrics, DB/checker outputs, or leaderboard outputs.
- Do not run DB/checker execution.
- Do not create `evidence/cases/` packages.
- Use explicit `git add` only.

Required preflight:
- Read project-control files.
- Read Wave A post-conversion parity review outputs.
- Read Common-core 40 conversion plan outputs.
- Confirm branch and clean worktree.

Required output:
- A Wave B audit directory under `audits/` with conversion status, manifest consistency audit, schema grouping decisions, cleanup deletion manifest, manual-review blockers, validator results, protected boundary checks, summary JSON, and command log.

Validation:
- Run static v2 validator for all converted Wave B cases.
- Re-run static v2 validator for accepted pilot and Wave A cases.
- Run `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Run `git diff --check` and boundary checks.
