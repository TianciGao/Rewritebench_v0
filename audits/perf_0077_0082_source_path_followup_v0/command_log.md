# Command Log

Commands and outcomes:

- `git status -sb`: clean worktree on `feature/case-package-v2-external-schema`.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -8`: reviewed latest branch history.
- Read project-control files: `MIGRATION_MASTER_PLAN.md`, `MIGRATION_STATUS.md`, `DECISION_LOG.md`, and `MIGRATION_RUN_LOG.md` tail.
- Read current target manifests and source SQL for `PERF_0077` and `PERF_0082`.
- `find cases/PERF/PERF_0077 cases/PERF/PERF_0082 -maxdepth 3 -type f`: confirmed no current case-local provenance/metadata files are present.
- `rg` searches for `PERF_0077`, `PERF_0082`, `source_path`, `manual_review_required`, `source_entry`, `JOB_DRAFT_0003`, `JOB_DRAFT_0005`, `3a.sql`, and `5a.sql`: found existing caveat tracking and no exact recovered source path.
- `git show 42ef246^:cases/PERF/PERF_0077/metadata/provenance.yaml`: branch-history provenance has `source_entry: ''` and `source_materialization: legacy case-local source.sql`.
- `git show 42ef246^:cases/PERF/PERF_0082/metadata/provenance.yaml`: branch-history provenance has `source_entry: ''` and `source_materialization: legacy case-local source.sql`.
- `git show 42ef246^:cases/PERF/PERF_0077/manifest.yaml` and `git show 42ef246^:cases/PERF/PERF_0082/manifest.yaml`: pre-v2 manifests also have blank `source_entry`.
- Read manifest caveat closeout CSVs, Wave C source-path follow-up CSV, final closeout rerun source-path follow-up CSV, case registry rows, source registry rows, and Common-core case-set rows.
- Decision: no manifest field repair; close both cases in this audit as retained nonblocking source-path provenance uncertainty without fabricating an exact path.

- `git diff --check`: passed.
- YAML parse check for `cases/PERF/PERF_0077/manifest.yaml` and `cases/PERF/PERF_0082/manifest.yaml`: passed.
- JSON parse/assertion for `source_path_followup_summary.json`: passed.
- CSV parse/header check for `source_path_followup_summary.csv`: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0077`: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case cases/PERF/PERF_0082`: passed.
- Static v2 validators for all 40 Common-core case packages: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -v`: passed, 19 tests.
- Protected-surface diff check: passed; no README, SQL, schema, checker, validation, case-set, inventory, reports/results, denominator, paper-result, case-membership, or raw retained-evidence files changed.
