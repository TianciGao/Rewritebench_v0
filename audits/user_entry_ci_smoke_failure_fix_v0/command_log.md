# Command Log

## Preflight

- `git status -sb`: clean on `feature/case-package-v2-external-schema`.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: confirmed latest U6 commits.

## GitHub Actions Inspection

- `gh run view 26206722303 --repo TianciGao/Rewritebench_v0 --json status,conclusion,name,headBranch,event,jobs`: not available because `gh` is not installed.
- `curl https://api.github.com/repos/TianciGao/Rewritebench_v0/actions/runs/26206722303/jobs`: succeeded and confirmed job `B-line user-entry smoke` failed at step `Run B-line user-entry smoke`.
- `curl https://api.github.com/repos/TianciGao/Rewritebench_v0/actions/jobs/77108078205/logs`: blocked with GitHub API `403`; job logs require repository admin rights from this environment.

## Local Reproduction

- `python scripts/dev/run_user_entry_ci_smoke.py`: passed in the existing local environment.
- Fresh venv with `pip install -e .`: reproduced failure. `pytest` and `yaml` were absent; the smoke script fell back to `unittest`; three U5 tag-slice tests failed because retained manifest taxonomy was not parsed with full YAML semantics.
- Fresh venv with `pip install -e . pytest`: still failed because `yaml` was absent.
- Fresh venv with `pip install -e . pytest PyYAML`: passed.

## Fix Validation

- `python scripts/dev/run_user_entry_ci_smoke.py`: passed after the patch.
- `runs/user/ci_smoke_dry_run` and `runs/user/ci_smoke_adapter`: removed by the patched smoke script after validation.

Final validation results are recorded in `protected_surface_check.md`.
