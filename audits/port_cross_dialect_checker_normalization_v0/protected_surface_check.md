# Protected Surface Check

## Allowed Modified Paths

- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/user_run.py`
- tests under `tests/user_entry/`
- `audits/port_cross_dialect_checker_normalization_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Surfaces

No changes are allowed to SQL files, manifests, schema files, checker config files, validation files, `case_sets/`, reports/results, denominator scaffolds, paper results, raw retained evidence, docs, examples, scripts, workflows, root metadata, release tags, or release branches.

## Validation Result

- `git diff --check`: passed.
- Python compile for modified source files: passed.
- Environment check: PostgreSQL probe ok; MySQL probe ok; Spark deferred/fail-closed.
- Help commands: passed.
- `tests/user_entry`: passed, 95 passed and 2 skipped.
- Current v2 static validation over all 40 Common-core case paths: passed.
- Audit CSV/JSON parse checks: passed.
- Audit Markdown sanity checks: passed.
- Protected-surface diff check: passed.
- Staged-file check before commit: passed; no files were staged during validation.
- `runs/user/port_pg_target_reference_normalized/`: ignored local output only, not staged.

Confirmed unchanged protected surfaces:

- SQL files: unchanged.
- Manifest files: unchanged.
- Schema files: unchanged.
- Checker config files: unchanged.
- Validation files: unchanged.
- `case_sets/`: unchanged.
- `reports/` and `results/`: unchanged.
- Denominator scaffolds: unchanged.
- Paper results: unchanged.
- Raw retained evidence: unchanged.
