# Validation Plan

## Current Behavior-Preservation Commands

Run these after a future minimal implementation split:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u2_split_dry_run --dry-run
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u2_split_dummy_adapter
PYTHONPATH=src pytest tests/user_entry
git diff --check
```

The generated `runs/user/u2_split_dry_run` and `runs/user/u2_split_dummy_adapter` directories must be removed after validation and must not be committed.

## Future Minimal Implementation Validation

Add or update tests for:

- Resolver success on `PERF_0006` and `CONS_0005`.
- Resolver fail-closed behavior on missing manifest/source/schema/checker paths.
- Adapter runner environment variables.
- Adapter runner `shell=False` and repository-root cwd behavior.
- Candidate capture priority: workspace `candidate.sql` before stdout.
- Adapter failure and timeout status mapping.
- Ledger writer preservation of current `LEDGER_FIELDS` and `FAILURE_FIELDS`.
- Dry-run rows preserving current status values.
- Output root remaining under `runs/user/{run_name}/`.

## Protected-Surface Checks

For this U2 design task, only these paths may change:

- `audits/user_entry_module_split_design_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Future implementation tasks may modify source/tests only if explicitly authorized. Even then, they must not modify cases, manifests, SQL, schemas, checker files, validation files, case sets, inventory, reports, results, denominator scaffolds, paper results, or raw retained evidence.

## DB/Checker Non-Requirement For U2

U2 is design-only and does not require DB/checker execution. Future minimal split validation should not require live PostgreSQL unless the implementation task explicitly opts into optional local diagnostics. Public smoke must remain non-DB by default.

## Run-Output Cleanup Rule

Any `runs/user/...` output created during future validation is local diagnostic output only. It must be removed after recording validation results and must not be committed.
