# User-Entry CI Smoke Failure Fix

## Scope

This packet records the narrow fix for the failed `user-entry-smoke` GitHub Actions run `26206722303`.

The task changed only CI smoke hygiene and project-control/audit records. It did not change user-entry runtime behavior, case packages, case sets, reports, results, denominator scaffolds, paper results, retained evidence, official metrics, or leaderboard output.

## Root Cause

The failed Actions job ran after an editable install with no dev/test dependencies. In a fresh editable-install environment without PyYAML, `scripts/dev/run_user_entry_ci_smoke.py` falls back to the installed dependency set and the U5 tag-slice tests fail because retained manifest taxonomy is not parsed with full YAML semantics.

Local reproduction without PyYAML failed with three `tests/user_entry/test_tag_slices.py` failures. Installing `pytest` and `PyYAML`, matching the intended user-entry test environment, made the CI smoke pass.

## Fix

- `.github/workflows/user_entry_smoke.yml` now installs `pytest` and `PyYAML` before running the B-line smoke script.
- `scripts/dev/run_user_entry_ci_smoke.py` now expects U4/U5 smoke outputs: `quality_summary.json`, `quality_report.md`, and `tag_slices.csv`.
- `scripts/dev/run_user_entry_ci_smoke.py` now removes its own `runs/user/ci_smoke_dry_run` and `runs/user/ci_smoke_adapter` outputs before checking `runs/user` cleanliness.

## Verdict

Local validation passed. The fix is CI-smoke scoped and does not advance U7.
