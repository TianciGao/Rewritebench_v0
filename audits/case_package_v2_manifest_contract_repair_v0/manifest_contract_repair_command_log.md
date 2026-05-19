# Manifest Contract Repair Command Log

- `pwd`; `git branch --show-current`; `git remote -v`; `git status -sb`; `git log --oneline -5`: preflight confirmed release repo branch and clean start.
- Read project-control files, v2 specs, accepted pilot/Wave A/Wave B audits, validator, tests, and the 32 target case packages.
- Used `git rev-list` and `git show` against this branch history to recover deleted `metadata/taxonomy.yaml` and `metadata/provenance.yaml` content for the 32 converted cases.
- Updated the v2 static validator to enforce the semantic manifest contract and regeneration-first evidence policy.
- Rewrote the 32 target manifests to semantic object-form manifests while preserving clean-template physical paths.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>` for all 32 repaired cases: passed.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 15 tests.
- JSON assertion for `manifest_contract_repair_summary.json`: passed.
- Boundary checks: no `case_sets/`, inventory, reports/results, denominator, paper-result, official-metric, DB/checker, or leaderboard surfaces changed.
- `git diff --stat`: reviewed.
- `git diff --check`: passed.
- `git status -sb`: reviewed.
