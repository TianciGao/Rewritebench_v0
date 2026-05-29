# PORT_0005 Conversion Command Log

Commands and short outcomes only.

- `pwd`: confirmed `/home/tianci_gao/code/Rewritebench_v0`.
- `git branch --show-current`: confirmed `feature/case-package-v2-external-schema`.
- `git remote -v`: confirmed `origin` remote.
- `git status -sb`: clean before task.
- `git log --oneline -5`: latest commit `92303b0 fix: adopt v2 three-file validation contract`.
- Read project-control files, Wave C preclearance artifacts, validation contract repair artifacts, manifest repair/caveat outputs, v2 specs, converted templates, and target `PORT_0005` case files.
- Created `schemas/parrot_bird_port0005_v0/` by copy-first schema extraction from case-local DDL/load.
- Created direct `sql/pos_01.sql` and `sql/neg_01.sql`; retained `sql/dialect_variants/spark/`.
- Repaired `manifest.yaml`, checker configs, schema profile, README, and source-as-oracle witness profile.
- Added three-file validation contract files under `cases/PORT/PORT_0005/validation/`.
- Deleted only `PORT_0005` v1 compatibility surfaces: nested SQL dirs, case-local engine schema dirs, case-local evidence, metadata, notes, data, and old engine-specific validation scripts.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PORT/PORT_0005`: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <32 converted cases>`: passed for 32/32.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion for `port0005_conversion_summary.json`: passed.
- CSV parse/header checks for generated audit CSVs: passed.
- Final static validators for `PORT_0005` plus 32 converted cases: passed, 33/33.
- Final unit tests: passed, 19 tests.
- Boundary checks: no other Wave C, pilot, Wave A, Wave B, `case_sets/`, inventory, reports/results, denominator, paper-result, `evidence/cases/`, DB/checker execution, official metric, or leaderboard changes.
- `git diff --stat`: reviewed.
- `git diff --check`: passed.
- `git status -sb`: reviewed before staging.
