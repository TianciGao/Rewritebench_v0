# Case Package v2 External-schema Branch Pilot Command Log

This log records short command outcomes only. It does not include secrets, raw long stdout/stderr dumps, DB credentials, or environment values.

## Preflight and Branch

- `pwd && git branch --show-current && git remote -v && git status -sb && git log --oneline -5 && git rev-list --left-right --count HEAD...origin/main`: passed; repo was clean on `main` and aligned with `origin/main`.
- `git branch --list feature/case-package-v2-external-schema`: no existing branch found.
- `git checkout -b feature/case-package-v2-external-schema`: passed.
- `git branch --show-current`: confirmed `feature/case-package-v2-external-schema`.

## Files Read

- Project control files: read.
- v1 case package specs and package validation schema: read.
- Common-core case-set and denominator metadata: read.
- User-runner, postgres execution, local checker, and run-artifact policy context: read.
- `PERF_0006` README, manifest, SQL, schema, checker, evidence, metadata, validation, and runs-retention files: read-only before edits.

## Pilot Conversion

- Created direct SQL copies: `sql/pos_01.sql` and `sql/neg_01.sql`.
- Created external schema copy under `schemas/tpch_common_core_v0/` for postgres, mysql, and spark DDL/load files.
- Created `schemas/tpch_common_core_v0/schema_profile.yaml`.
- Added manifest `schema_ref` for `tpch_common_core_v0`.
- Created `witness/data_profile.yaml` and `witness/correct_result.csv`.
- Created `validation/run_validation.sh` and `validation/run_plan_collection.sh` wrappers that do not run DB engines or write case-local runs during the branch pilot.
- Retained old `sql/positives/`, `sql/negatives/`, `schema/`, and `runs/` paths for compatibility.
- Recorded decision `D019` in `project_control/DECISION_LOG.md`.

## Validation

- YAML parse for `cases/PERF/PERF_0006/manifest.yaml`: passed.
- YAML parse for `schemas/tpch_common_core_v0/schema_profile.yaml`: passed.
- YAML parse for `cases/PERF/PERF_0006/witness/data_profile.yaml`: passed.
- Static path checks for v2 SQL, witness, checker, runs retention, and external schema files: passed.
- Optional non-DB user-entry CI smoke: help/tests/dry-run/dummy-adapter portions passed, then expectedly failed the protected-path guard because this branch intentionally modifies `cases/PERF/PERF_0006`.
- `git status --short case_sets inventory reports results`: passed; no protected metadata/report/result changes.
- `git status --short cases`: passed; case-package changes are limited to `cases/PERF/PERF_0006/`.
- `git diff --check`: passed.

## Boundaries

- Legacy repo inspected: no.
- Legacy repo modified: no.
- Cases modified: `PERF_0006` only.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Raw legacy evidence changed: no.
- Official metrics computed: no.
- Paper tables rendered: no.
- Global leaderboard created: no.
