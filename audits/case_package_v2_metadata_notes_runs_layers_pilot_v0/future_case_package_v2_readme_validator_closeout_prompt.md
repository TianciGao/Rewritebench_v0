# Future Prompt: case_package_v2_readme_validator_closeout_pilot_v0

Work only in `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`. Do not modify `main` and do not inspect or modify the legacy repository.

This is a branch-only README/validator closeout pilot for exactly:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Scope:

- Update README wording only to describe the completed v2 layer status.
- Update static validator expectations only if existing checks produce false positives against the approved v2 folder-ordered contract.
- Do not convert additional case assets.
- Do not delete evidence or runs.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not modify reports/results, denominators, paper results, case sets, inventory, or leaderboard outputs.

Required validation:

- Run `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>` for each pilot case.
- Run `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`.
- Confirm no protected benchmark-surface changes.

Stop conditions:

- Any DB/checker execution.
- Any official metric computation.
- Any evidence deletion or non-empty runs deletion.
- Any reports/results, denominator, paper-result, case-set, inventory, or leaderboard change.
