# PERF_0006 Format Normalization Command Log

Commands are summarized. No secrets, DB credentials, raw long outputs, DB/checker execution, metric computation, paper rendering, or leaderboard creation occurred.

## Preflight

- `pwd`: confirmed `/home/tianci_gao/code/Rewritebench_v0`.
- `git branch --show-current`: confirmed `feature/case-package-v2-external-schema`.
- `git remote -v`: confirmed `origin` remote.
- `git status -sb`: confirmed clean branch before edits.
- `git log --oneline -5`: reviewed recent v2 branch commits.
- `git rev-list --left-right --count HEAD...origin/feature/case-package-v2-external-schema`: confirmed branch was not ahead or behind origin.

## Read-only Review

- Read v2 project-control files, repository specs, prior validator audit outputs, PERF_0006 manifest/README, schema profile, resolver, validator, and tests.
- Inspected case-local schema, evidence, validation, and witness file presence.

## Edits

- Updated `cases/PERF/PERF_0006/manifest.yaml` to canonical v2 internal reference shape.
- Updated `cases/PERF/PERF_0006/README.md` with a minimal canonical-manifest status note.
- Added `compatibility` to the v2 resolver compatibility top-level key set after the normalized manifest exposed a validator false positive.
- Updated the read-only PERF_0006 unit assertion because the normalized manifest now produces zero format findings.
- Created this audit packet.

## Validation

- Manifest canonical-shape Python assertion: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0006`: passed.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed.
- Summary JSON parse and boundary assertions: passed.
- Protected boundary checks: passed.
- `git diff --check`: passed.
- `git status -sb`: reviewed before staging and commit.
