# Command Log: case_package_v2_metadata_notes_runs_layers_pilot_v0

Commands are summarized. No secrets, credentials, full DSNs, or long raw outputs are recorded.

## Preflight and Read-only Review

- `pwd && git branch --show-current && git remote -v && git status -sb && git log --oneline -5`: confirmed repository root, branch `feature/case-package-v2-external-schema`, clean status, and current branch history.
- Read project-control files, v2 specs, prior v2 pilot summaries, and the five pilot case directories.
- Inventoried `metadata/`, `notes/`, and `runs/` for all five cases.
- Ran a hygiene scan over case-local metadata and notes; no credentials, private local paths, API keys, prompts, model traces, or raw debug traces were selected for copy.

## Writes

- Copied public-safe case-local note files into `evidence/cases/<POOL>/<CASE_ID>/notes/` for all five cases.
- Updated the five pilot manifests with `compatibility.metadata_legacy`, `compatibility.notes_legacy`, and `compatibility.runs_legacy`.
- Created this audit packet.
- Updated `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md`.

## Validation

- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0006`: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0007`: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/CONS/CONS_0005`: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PORT/PORT_0003`: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/LONGTAIL/LONGTAIL_0011`: passed.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed.
- Summary JSON parse and boundary assertions: passed.
- Protected path checks: passed.
- `git diff --check`: passed.
