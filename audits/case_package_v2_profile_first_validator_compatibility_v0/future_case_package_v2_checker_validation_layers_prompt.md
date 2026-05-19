# Future Prompt: case_package_v2_checker_validation_layers_pilot_v0

Work only in `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`. Do not modify `main` and do not inspect or modify the legacy repository.

This is a branch-only writable pilot for the next folder-order layers after profile-first schema validator compatibility:

1. checker
2. validation

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Scope:

- Normalize `checker/` references and config names only where safe.
- Add or normalize `validation/run_validation.sh` and `validation/run_plan_collection.sh` as thin wrappers.
- Keep old engine-specific validation scripts as compatibility assets unless wrapper equivalence and deletion approval are explicit.
- Do not modify witness, evidence, metadata, notes, runs, case sets, inventory, reports, results, denominators, paper results, or schemas except if a checker/validation path reference requires a documented non-destructive manifest compatibility update.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not create leaderboard output.

Required validation:

- Run `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Run `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>` for each pilot case.
- Confirm no protected paths changed outside the authorized case checker/validation files and audit/project-control outputs.

Stop conditions:

- Any case-local runs deletion.
- Any evidence deletion or retained-evidence parsing.
- Any output under `runs/user/` or case-local `runs/`.
- Any DB/checker execution.
- Any denominator, paper result, reports/results, case_sets, or inventory change.
- Any global leaderboard output.
