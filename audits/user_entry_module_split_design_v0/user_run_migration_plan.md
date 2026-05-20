# User Run Migration Plan

## Current Responsibilities Inside `user_run.py`

Current `user_run.py` owns:

- CLI parsing.
- Output-root validation.
- Config writing.
- Selected-case CSV writing.
- Adapter environment construction.
- Adapter subprocess invocation.
- Candidate capture priority.
- Dry-run ledger row construction.
- Base ledger row construction.
- Optional DB/checker orchestration.
- Ledger/failure CSV writing.
- Summary JSON construction.
- Report Markdown construction.
- Top-level command exit behavior.

This is workable for the current MVP but too broad for the planned local diagnostic harness.

## Proposed Extraction Order

1. Extract `case_package_resolver.py` with tests that resolve smoke cases and fail closed on missing package assets.
2. Extract `adapter_runner.py` by moving `_build_env` and `_run_adapter_for_row` behavior without changing capture semantics.
3. Extract `user_ledger.py` by moving `_ledger_base`, dry-run row creation, failure-row creation, and CSV writer ownership.
4. Keep `_summary_payload` and `_write_report` in `user_run.py` until `user_quality_report.py` is separately authorized.
5. Keep optional PostgreSQL/checker orchestration in `user_run.py` until the future engine-router phase.

## Behavior-Preserving Steps

Step A: Resolver extraction.

- Add `ResolvedCasePackage`.
- Resolve `manifest.yaml`, source SQL, schema profile, external schema profile, and checker config paths.
- Call resolver after selection but before adapter invocation.
- Keep selected row fields unchanged.
- Do not change output schema.

Step B: Adapter runner extraction.

- Move adapter environment creation and subprocess invocation into `adapter_runner.py`.
- Preserve `shell=False`, repository-root cwd, stdout/stderr paths, timeout behavior, and candidate capture priority.
- Preserve status strings in `user_run_schema.py`.
- Keep dry-run behavior outside adapter runner.

Step C: Ledger writer extraction.

- Move base ledger row, dry-run row, failure row, `ledger.csv`, and `failures.csv` writing into `user_ledger.py`.
- Keep summary/report generation unchanged.
- Preserve existing `LEDGER_FIELDS` and `FAILURE_FIELDS`.

Step D: Rewire `user_run.py`.

- Keep CLI and orchestration readable.
- Use explicit handoffs between selection, resolver, adapter runner, optional DB/checker, and ledger writer.
- Avoid changing public command output text unless tests authorize it.

## Test Gates After Each Step

Run after each extraction:

- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`
- `python scripts/user/run_user_benchmark.py --help`
- public smoke dry-run with `--smoke --dry-run`
- public smoke adapter-capture with `--smoke`
- `PYTHONPATH=src pytest tests/user_entry`
- protected-surface check for no cases/case_sets/reports/results changes
- cleanup check for generated `runs/user/...` outputs

Additional targeted tests:

- Resolver resolves `PERF_0006` and `CONS_0005`.
- Resolver fails closed for a missing manifest/source/checker path fixture.
- Adapter runner captures workspace `candidate.sql` before stdout.
- Adapter runner records non-zero exit and timeout.
- Ledger writer preserves current `ledger.csv` and `failures.csv` columns.

## Rollback Strategy

Keep each extraction in a separate minimal commit during implementation. If any behavior-preservation gate fails, revert the extraction commit rather than patching across unrelated modules.

Do not combine resolver, adapter runner, ledger writer, preflight, quality report, tag slicing, or timing changes in one implementation commit.

## Risks of Over-Refactor

- Moving summary/report generation too early could change public output format.
- Moving DB/checker orchestration before an engine-router design could destabilize optional PostgreSQL diagnostics.
- Adding preflight fields during the split could break U1-compatible CSV consumers.
- Introducing tag/timing concepts during the split could blur local diagnostics with official metrics.
- Large refactors make smoke regressions harder to isolate.
