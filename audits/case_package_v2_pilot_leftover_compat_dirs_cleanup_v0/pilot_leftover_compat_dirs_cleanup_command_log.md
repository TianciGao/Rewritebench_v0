# Pilot Leftover Compatibility Directories Cleanup Command Log

Commands and outcomes:

- `pwd`: confirmed `/home/tianci_gao/code/Rewritebench_v0`.
- `git branch --show-current`: confirmed `feature/case-package-v2-external-schema`.
- `git remote -v`: confirmed `origin` points to `git@github.com:TianciGao/Rewritebench_v0.git`.
- `git status -sb`: clean before cleanup.
- `git log --oneline -5`: latest commit was Common-core 40 v2 final closeout audit.
- Read project-control files and final-closeout blocker artifacts.
- Inspected all 15 candidate directories: all existed and were empty.
- Checked target case files for live references to `notes/`, `sql/positives/`, and `sql/negatives/`: none found.
- `rmdir` on all 15 candidate directories: succeeded.
- Static v2 validators for five target cases: passed.
- Static v2 validators for all 40 Common-core cases: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Summary JSON assertion: passed.
- CSV parse/header checks: passed.
- Candidate directory absence check: passed for all 15 deleted directories.
- `PORT_0003` dialect variant retention check: passed.
- `git diff --check`: passed.
- No DB/checker execution, official metrics, reports/results update, denominator update, paper-result change, leaderboard creation, `evidence/cases/` creation, or dialect-variant deletion was performed.
