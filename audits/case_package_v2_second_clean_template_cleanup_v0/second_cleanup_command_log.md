# Second Clean-template Cleanup Command Log

- `pwd && git branch --show-current && git remote -v && git status -sb && git log --oneline -5` - confirmed branch `feature/case-package-v2-external-schema`, clean preflight, and origin remote.
- Read readiness CSVs from `audits/case_package_v2_validation_evidence_unblock_v0/` - selected 50 readiness-marked cleanup candidates.
- `find` and `rg` over the five pilot cases - inspected candidate paths and stale references.
- Python verification script - confirmed v2 wrappers do not call legacy scripts, external schema DDL/load files match case-local copies, and case-local evidence files map byte-for-byte to external evidence packages.
- Python cleanup script - updated manifest/README compatibility wording and deleted 30 legacy validation scripts, 15 schema engine directories, and 5 case-local evidence directories.
- Five `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case ...` commands - all passed.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v` - passed 9 tests.
- Removed generated `__pycache__/` directories after tests.
- Created second-clean-template cleanup audit outputs.
- JSON assertion, `git diff --check`, boundary checks, commit, and push recorded after final validation.
