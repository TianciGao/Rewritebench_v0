# Command Log

Commands are summarized without secrets, private environment values, long stdout/stderr dumps, or legacy-repository access.

- `pwd` / `git branch --show-current` / `git remote -v` / `git status -sb` / `git log --oneline -5`: confirmed release repo and branch `feature/case-package-v2-external-schema`.
- Read project-control, repository spec, prior audit, resolver, validator, test, manifest, and schema-profile files listed in the task.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed; 9 tests.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0006`: passed; `overall_status=pass`.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0007`: passed; `overall_status=pass` with expected warning-only later-layer findings.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/CONS/CONS_0005`: passed; `overall_status=pass` with expected warning-only later-layer findings.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PORT/PORT_0003`: passed; `overall_status=pass` with expected warning-only later-layer findings.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/LONGTAIL/LONGTAIL_0011`: passed; `overall_status=pass` with expected warning-only later-layer findings.
- Summary JSON boundary assertions: passed.
- Protected path checks: passed; no tracked changes under `cases/`, `schemas/`, `case_sets/`, inventory, reports, or results.
- `git diff --check`: passed.
- `git commit -m "dev: support profile-first v2 schema refs"`: created commit `dc07170d9b2776aeff17ffebdce0b5239b181ca3`.
- `git push origin feature/case-package-v2-external-schema`: succeeded.
