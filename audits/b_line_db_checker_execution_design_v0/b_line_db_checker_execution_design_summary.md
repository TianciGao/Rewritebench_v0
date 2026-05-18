# B-line DB/Checker Execution Design v0

## Purpose and Scope

This packet designs the next B-line layer for local user-run DB execution and checker evaluation. It is design-only. It does not implement DB execution, checker execution, timing, official metric computation, paper table rendering, paper reproduction, retained-evidence adapters, SQLGlot execution evaluation, Calcite or R-Bot routes, case migration, case-set updates, denominator updates, reports/results migration, leaderboard output, or raw legacy evidence modification.

The design preserves the existing user-run output boundary: all future local execution artifacts must stay under `runs/user/<run_id>/`, must not be written into case-local `runs/`, and must not become retained paper evidence unless a separate retained-evidence task explicitly authorizes that path.

## Current User-entry and SQLGlot Status

The B-line user-entry runner currently supports metadata-driven Common-core v0 selection, optional pool and case-list filtering, engine selection, adapter invocation, candidate SQL capture, dry-run mode, and local outputs under `runs/user/<run_id>/`. The runner writes `config.yaml`, `selected_cases.csv`, `candidate_sql/`, `workspaces/`, `ledger.csv`, `summary.json`, `failures.csv`, and `report.md`.

The SQLGlot adapter layer now has two optional candidate-generation routes:

- `sqlglot_noop`
- `sqlglot_optimize`

The SQLGlot-enabled smoke installed `.[sqlglot]`, imported SQLGlot, and generated candidate SQL for `PERF_0006` and `PERF_0007` postgres rows through both routes. That smoke did not execute SQL, run checkers, collect timing, compute metrics, update retained evidence, update reports/results, or create a leaderboard.

## Why Design Comes Before Implementation

DB and checker execution introduce external state, credentials, schema setup, engine-specific result rendering, timeouts, cleanup requirements, and stricter failure semantics. A design packet is needed before implementation so the project can preserve the boundary between local user experiments and official paper evidence. The design also keeps default CI non-DB, avoids accidental reports/results writes, and defines fail-closed behavior for missing checker or normalization configs before any engine code exists.

## Future MVP Scope

The recommended future DB/checker MVP is deliberately narrow:

- Case set: Common-core v0 only.
- Engine: postgres only.
- Initial cases: 1-2 PERF cases, preferably `PERF_0006` and `PERF_0007`.
- Candidate route: SQLGlot no-op first, because candidate generation is already validated.
- Execution: run source SQL and candidate SQL in a local postgres environment only after explicit authorization.
- Checker: invoke only if the case package provides safe `checker/checker.yaml`, `checker/normalization.yaml`, and `checker/compare_config.yaml`.
- Output root: `runs/user/<run_id>/` only.
- Timing: not collected.
- Official metrics: not computed.
- Reports/results: not updated.
- Retained evidence: not updated.
- Denominators and paper results: unchanged.
- Leaderboard: not created.

MySQL, Spark, timing, official metrics, paper reproduction, retained-evidence integration, Calcite, R-Bot, and broad case/pool expansion are later phases and need separate authorization.

## Engine Runner Boundary

A future engine runner should be a small, replaceable component with explicit input and output boundaries. It should not infer benchmark membership by scanning case directories.

Required future fields:

- `engine_id`: one of the authorized engine ids for the MVP scope.
- `connection_config_source`: environment variables or local config excluded from git.
- `schema_setup_command_boundary`: apply `schema/<engine>/ddl.sql` and `schema/<engine>/load.sql` in an isolated local schema or database.
- `source_sql_execution_command_boundary`: execute `sql/source.sql` after schema setup.
- `candidate_sql_execution_command_boundary`: execute the captured candidate SQL for the selected row.
- `timeout_policy`: fail closed on source, candidate, checker, or cleanup timeout.
- `result_capture_format`: normalized intermediate JSONL, plus raw local DB result if retained only as local artifact.
- `error_capture_format`: local text or JSON diagnostics under the row workspace.
- `cleanup_policy`: clean transient schema/database state for the row or run; record cleanup failure as local diagnostic.
- `artifact_directory`: `runs/user/<run_id>/workspaces/<case_id>/<engine>/execution/`.

DB credentials must never be committed. Engine connection config must come from environment variables or local config files excluded from git. DB outputs are local user experiment artifacts, not retained paper evidence.

## Source and Candidate SQL Execution Contract

For each selected row, the future runner should execute source SQL and candidate SQL against the same local engine context after schema setup. The source query provides the local reference result for that run; it is not a paper retained-evidence refresh. Candidate SQL comes from `candidate_sql/<case_id>__<engine>.sql` or the per-row workspace `candidate.sql`.

Execution must fail closed when:

- schema assets are missing for the selected engine;
- local engine configuration is unavailable;
- schema setup fails;
- source execution fails;
- candidate execution fails;
- execution exceeds timeout;
- output paths would escape `runs/user/<run_id>/`;
- a result file would overwrite case-package or reports/results surfaces.

## Checker Invocation Contract

The future checker runner should consume:

- source result artifact path;
- candidate result artifact path;
- `checker/checker.yaml`;
- `checker/normalization.yaml`, when present;
- `checker/compare_config.yaml`, when present;
- case metadata from the selected case package;
- engine id;
- output artifact directory under the per-row workspace.

Future checker outputs:

- `checker_status`;
- `exact_status`;
- `mismatch_summary` path;
- `normalized_source_result` path;
- `normalized_candidate_result` path;
- `checker_log` path;
- `failure_bucket`;
- `notes`.

If checker config, normalization config, or compare config is required but missing, the checker must not guess semantics. It should record `checker_config_missing` or `normalization_config_missing` and stop for that row.

## Normalization Contract

Normalization must be driven by case-package config, not global assumptions. Future runner behavior should interpret:

- row ordering: sort only when the normalization config says unordered or sort is allowed;
- duplicate handling: preserve duplicates unless config explicitly treats rows as sets;
- numeric tolerance: use case config, such as exact-after-normalization or a numeric tolerance value;
- NULL representation: normalize only according to the case config;
- date/time normalization: preserve text unless config defines an engine-safe conversion;
- string/case normalization: preserve case unless config defines a rule;
- engine-specific caveats: record unsupported or ambiguous types rather than coercing silently.

If a case lacks normalization config for result comparison, the future checker MVP should fail closed with `normalization_config_missing` and `not_evaluated_checker_missing`. It should not infer equivalence from raw textual equality unless that behavior is explicitly authorized for the case.

## Ledger Schema Extension

The current user-run `ledger.csv` is one row per selected case-engine row and records adapter/candidate capture plus non-DB status placeholders. The future DB/checker MVP should extend that row grain rather than creating a separate official metric ledger.

Proposed future fields include:

- `execution_enabled`
- `checker_enabled`
- `source_execution_status`
- `candidate_execution_status`
- `source_result_path`
- `candidate_result_path`
- `checker_config_path`
- `normalization_config_path`
- `compare_config_path`
- `execution_failure_class`
- `checker_failure_class`
- `mismatch_artifact_path`
- `db_artifact_dir`
- `local_execution_only`
- `official_metric_input`
- `retained_evidence_input`

For the future user-run MVP, `local_execution_only=true`, `official_metric_input=false`, and `retained_evidence_input=false` are required boundary fields.

## Status and Failure Bucket Vocabulary

Execution status values:

- `not_run_non_db_mvp`
- `execution_not_enabled`
- `source_execution_success`
- `candidate_execution_success`
- `source_execution_failed`
- `candidate_execution_failed`
- `execution_timeout`
- `execution_unsupported`
- `execution_internal_error`

Checker status values:

- `not_run_non_db_mvp`
- `checker_not_enabled`
- `checker_success`
- `checker_mismatch`
- `checker_failed`
- `checker_timeout`
- `checker_unsupported`
- `checker_config_missing`
- `normalization_config_missing`
- `checker_internal_error`

Exact status values:

- `not_evaluated_non_db_mvp`
- `exact`
- `mismatch`
- `not_exact_due_to_execution_failure`
- `not_exact_due_to_checker_failure`
- `not_exact_due_to_timeout`
- `not_evaluated_checker_missing`

Failure buckets:

- `none`
- `adapter_failed`
- `no_candidate_sql`
- `source_execution_failed`
- `candidate_execution_failed`
- `execution_timeout`
- `checker_config_missing`
- `checker_failed`
- `checker_timeout`
- `mismatch`
- `unsupported_engine`
- `internal_runner_error`

## Output Policy

Future DB/checker local output structure:

```text
runs/user/<run_id>/
  config.yaml
  selected_cases.csv
  candidate_sql/
  workspaces/
  execution/
  checker/
  ledger.csv
  summary.json
  failures.csv
  report.md
```

Per-row workspace:

```text
workspaces/<case_id>/<engine>/
  candidate.sql
  adapter_stdout.txt
  adapter_stderr.txt
  execution/
    source_result.jsonl
    candidate_result.jsonl
    source_error.txt
    candidate_error.txt
  checker/
    checker_result.json
    mismatch_summary.json
    normalized_source_result.jsonl
    normalized_candidate_result.jsonl
```

These outputs are local user-run artifacts and must not be staged or committed by default. They must not be copied into case packages, `results/retained/`, `reports/evaluation/`, `reports/paper/`, or case-local `runs/`.

## Implementation Safety Gates

Before implementation, require:

- explicit maintainer authorization for a DB/checker MVP;
- engine environment availability check;
- local secrets policy for DB connection configuration;
- output-root guard revalidation;
- per-query timeout policy;
- schema setup and cleanup policy;
- checker config availability policy;
- fail-closed behavior for missing checker, normalization, or compare configs;
- protected-path checks for `cases/`, `case_sets/`, `inventory/`, `reports/`, and `results/`;
- no official metrics;
- no retained-evidence updates;
- no paper result updates;
- no denominator changes;
- no global leaderboard;
- default CI remains non-DB unless a manual opt-in workflow is separately authorized.

## Relationship to SQLGlot, Calcite, and R-Bot

The design should apply first to SQLGlot no-op and SQLGlot optimize because those candidate-generation routes already pass non-DB user-entry smoke. Calcite HEP should be later and fail-closed as a rule-based route. R-Bot should be later and bounded as a prior-system route.

This design does not rank methods and does not create a global leaderboard.

## Relationship to Official Metrics

Future DB/checker user-run output may support local diagnostics:

- candidate generation status;
- source and candidate execution status;
- checker/exact status;
- mismatch summaries;
- local report funnels.

This design does not compute official Generation Rate, Execution Coverage Rate, Result Consistency Rate, timing metrics, GM_Speedup, Speedup Ratio Percentiles, Cross-Engine metrics, or any paper table value. It does not write metric input rows unless a later task separately authorizes a bridge from local user-run diagnostics to a validated production ledger. It does not update paper results.

## No-global-leaderboard Boundary

Local user-run reports may summarize a single run. They must not compare unrelated methods as a global ranking, mix denominator families, or claim paper-result status. Any future report section must include local-output and no-leaderboard warnings.

## Representative Case Structure Review

The design reviewed one Common-core case package from each pool: `PERF_0006`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`. All inspected packages expose source SQL, positive rewrite SQL, checker config, normalization config, compare config, postgres schema DDL/load assets, denominator eligibility metadata, and runs-retention mappings. This supports the future MVP choice to begin with Common-core PERF postgres rows while preserving fail-closed behavior for missing or ambiguous configs.

## Exact Next Safe Action

Authorize `b_line_db_checker_execution_mvp_v0` as a separately bounded implementation only if the maintainer wants local DB/checker execution next. The recommended MVP should be postgres-only, Common-core v0 only, 1-2 PERF cases, SQLGlot no-op first, local `runs/user/<run_id>/` outputs only, no timing, no official metrics, no reports/results updates, no retained-evidence updates, no denominator changes, and no leaderboard.
