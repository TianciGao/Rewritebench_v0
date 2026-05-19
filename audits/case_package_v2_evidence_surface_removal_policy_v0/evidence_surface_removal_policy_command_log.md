# Evidence Surface Removal Policy Command Log

- Repository preflight: `pwd`, `git branch --show-current`, `git remote -v`, `git status -sb`, and `git log --oneline -5` confirmed the target repository/branch and expected branch history.
- `sed`/`rg` inspection: reviewed project-control files, v2 specs, resolver, tests, recent evidence cleanup audits, and five pilot case references.
- `find`/`rg` inspection: confirmed case-local `evidence/` is absent for all five pilot cases and top-level `evidence/cases/<POOL>/<CASE_ID>/` exists for all five.
- Updated resolver and tests: added regeneration-first `evidence_policy` support and optional `evidence_ref` behavior.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed 11 tests after evidence-policy test update.
- V2 validator for `PERF_0006`: passed.
- V2 validator for `PERF_0007`: passed.
- V2 validator for `CONS_0005`: passed.
- V2 validator for `PORT_0003`: passed.
- V2 validator for `LONGTAIL_0011`: passed.
- JSON summary assertion: passed.
- `git diff --check`: passed.
- Boundary status check: no `cases/`, `evidence/`, `case_sets/`, `inventory/`, `reports/`, or `results/` changes.
