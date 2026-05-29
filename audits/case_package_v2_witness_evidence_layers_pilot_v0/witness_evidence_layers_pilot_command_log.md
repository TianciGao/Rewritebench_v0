# Command Log: case_package_v2_witness_evidence_layers_pilot_v0

Commands are summarized. No secrets, credentials, full DSNs, or long raw outputs are recorded.

## Preflight and Read-only Review

- `pwd && git branch --show-current && git remote -v && git status -sb && git log --oneline -5`: confirmed repository root, branch `feature/case-package-v2-external-schema`, clean status, and current branch history.
- Read project-control files, v2 repository specs, prior audit packets, pilot manifests, and case witness/evidence inventories.
- `rg` hygiene scan over case-local evidence: found only benign policy/validation terms and a false stdout/stderr copy flag; no credentials, API keys, prompt traces, private local paths, or raw debug traces selected for copy.

## Writes

- Copied public-safe evidence from case-local `evidence/` to top-level `evidence/cases/<POOL>/<CASE_ID>/` for all five pilot cases.
- Added lightweight `witness/witness_profile.yaml` files for all five pilot cases.
- Updated the five pilot manifests with canonical source-as-oracle witness policy, `evidence_ref`, and compatibility witness/evidence blocks.
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
