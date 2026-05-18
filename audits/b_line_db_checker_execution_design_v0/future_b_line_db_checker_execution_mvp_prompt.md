# Future Prompt: b_line_db_checker_execution_mvp_v0

You are working on SQL-RewriteBench clean public release migration / redevelopment.

Task title:
`b_line_db_checker_execution_mvp_v0`

This is a bounded B-line DB/checker execution MVP implementation task.

This future task is not authorized by the current design packet. Execute it only if separately approved.

## Scope

Implement the smallest local DB/checker MVP:

- Common-core v0 only.
- Postgres only.
- 1-2 PERF cases only, preferably `PERF_0006` and `PERF_0007`.
- SQLGlot no-op candidate route first.
- Local user-run output only under `runs/user/<run_id>/`.
- Execute source SQL and candidate SQL only after local postgres environment checks pass.
- Invoke checker only when `checker/checker.yaml`, `checker/normalization.yaml`, and `checker/compare_config.yaml` are present.
- No timing collection.
- No official metric computation.
- No paper table rendering.
- No retained-evidence update.
- No reports/results update.
- No denominator change.
- No case-set or inventory update.
- No leaderboard.

## Required Boundaries

Do not:

- modify legacy repo;
- modify `cases/`;
- modify `case_sets/`;
- modify `inventory/`;
- modify `reports/`;
- modify `results/`;
- write into case-local `runs/`;
- change denominators;
- change paper results;
- compute official Generation Rate, Execution Coverage Rate, Result Consistency Rate, timing metrics, or speedup;
- create global leaderboard output;
- parse retained evidence;
- update retained evidence.

## Required Future Reads

Read:

- `audits/b_line_db_checker_execution_design_v0/b_line_db_checker_execution_design_summary.md`
- `audits/b_line_db_checker_execution_design_v0/db_checker_execution_contract.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_ledger_extension.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_status_vocabulary.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_output_policy.csv`
- `audits/b_line_db_checker_execution_design_v0/db_checker_safety_gates.csv`
- existing user-entry runner modules under `src/sql_rewrite_bench/`
- `docs/RUN_ARTIFACT_POLICY.md`
- `case_sets/common_core_v0/denominator_same_engine_120.csv`
- representative case files for the selected PERF cases

## Required Implementation Shape

Add implementation only after preflight confirms the repository is clean.

Recommended additions:

- a narrow postgres execution module under `src/sql_rewrite_bench/`;
- local result JSONL writer;
- checker-normalization module driven by case config;
- tests with mocked or explicitly opt-in postgres execution;
- manual local smoke command, not default CI;
- audit packet under `audits/b_line_db_checker_execution_mvp_v0/`.

## Validation Requirements

Validate:

- output root remains `runs/user/<run_id>/`;
- protected paths remain unchanged;
- ledger has `local_execution_only=true`;
- ledger has `official_metric_input=false`;
- ledger has `retained_evidence_input=false`;
- no timing fields are populated as metrics;
- no report claims leaderboard or paper result status;
- default CI remains non-DB.

## Stop Conditions

Stop if:

- postgres local environment is unavailable;
- credentials would need to be committed or logged;
- source/candidate execution would require writes outside `runs/user/`;
- checker or normalization config is missing;
- implementation would modify case packages, case sets, inventory, reports, results, denominators, paper results, retained evidence, or raw legacy evidence;
- official metric or leaderboard output becomes necessary.
