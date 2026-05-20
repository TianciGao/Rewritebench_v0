# User-Entry Local Evaluation Architecture Plan

## 1. Stage purpose

This stage upgrades the current smoke/user-entry path into a modular local diagnostic evaluation harness. The harness should let users run adapters over controlled Common-core v0 case-engine rows, capture candidate SQL, optionally execute local engine diagnostics, compare source/candidate results, and produce denominator-aware local summaries.

This stage remains distinct from:

- full paper reproduction
- official metrics computation
- paper table rendering
- retained-evidence adapter integration
- reports/results migration
- release export/tagging
- global leaderboard

The output of this stage is local diagnostic evidence under `runs/user/{run_name}/`, not retained paper evidence and not official benchmark results.

## 2. Locked benchmark boundaries

- Common-core v0 = 40 cases = 16 PERF + 9 CONS + 9 PORT + 6 LONGTAIL.
- Track A same-engine denominator = 120 planned rows.
- Case package is the benchmark unit.
- Results must be role-aware and denominator-aware.
- No global leaderboard.
- Performance is interpreted only on exact + timed rows.
- Hard negatives are checker controls, not method-generated failures.
- User-run outputs are local diagnostics only.

No user-entry implementation phase may change case membership, denominator values, paper results, reports/results, retained evidence, or raw legacy evidence.

## 3. Current implementation baseline

- `src/sql_rewrite_bench/user_run.py` is the current CLI and orchestrator.
- `src/sql_rewrite_bench/case_selection.py` selects rows from `case_sets/common_core_v0/`, not by scanning `cases/`.
- `examples/user/noop_adapter.py` is the public adapter smoke example.
- `src/sql_rewrite_bench/postgres_execution.py` exists as the current PostgreSQL local diagnostic executor.
- `src/sql_rewrite_bench/local_result_checker.py` exists as the result-consistency checker over local JSONL execution artifacts.
- Public `--smoke` works and selects `PERF_0006` and `CONS_0005` for the requested engine.
- Optional PostgreSQL/checker diagnostics are external-schema aware through manifest `schema.external_profile` and external schema metadata.
- Timing and official metrics are not implemented in user-entry.
- MySQL/Spark diagnostic execution is not yet implemented.

## 4. Target runtime pipeline

Target flow:

```text
CLI args
-> case selection
-> case package resolution
-> adapter runner
-> candidate preflight
-> engine execution router
-> engine-specific execution
-> local result checker
-> ledger/failure-bucket writer
-> local quality report
-> tag-aware slices
-> timing diagnostics later
```

Stage status:

- Current: CLI args, case selection, adapter invocation/capture, PostgreSQL diagnostic execution, local checker, basic ledger/failure rows, basic summary/report.
- Proposed next: explicit case package resolver, adapter runner module split, candidate preflight v0, ledger writer module, local quality report v0, tag-aware slices v0.
- Deferred: MySQL/Spark execution implementation, timing diagnostics, official metrics, paper reproduction, retained-evidence adapter integration, paper rendering.

## 5. Module responsibility table

| Responsibility | Current / future module | Owns | Must not own |
|---|---|---|---|
| CLI / orchestration | `src/sql_rewrite_bench/user_run.py` | CLI args, run setup, high-level orchestration, calling modules, writing run root. | SQL parsing details, result comparison logic, engine-specific details, metrics math. |
| Case selection | `src/sql_rewrite_bench/case_selection.py` | Selecting case-engine rows from `case_sets/common_core_v0/cases.csv` and `denominator_same_engine_120.csv`. | Deciding membership by scanning `cases/`, manifest parsing, checker logic. |
| Case package resolver | Proposed `src/sql_rewrite_bench/case_package_resolver.py` | Resolving `case_dir`, `manifest.yaml`, `sql/source.sql`, schema profile, checker paths, taxonomy/tag references. | Adapter execution, DB execution, metrics. |
| Adapter runner | Proposed `src/sql_rewrite_bench/adapter_runner.py` | Invoking user rewriter adapter, environment variables, stdout/stderr capture, `candidate.sql` capture. | SQL correctness, DB execution, checker. |
| Candidate preflight | Proposed `src/sql_rewrite_bench/candidate_preflight.py` | Empty SQL, missing SQL, unsafe SQL, multi-statement, unsupported statement type, parse status if parser exists, source-like/no-op flag. | Semantic equivalence, result consistency, performance. |
| Engine execution router | Proposed `src/sql_rewrite_bench/engine_execution.py` | Dispatch by engine to PostgreSQL/MySQL/Spark executors, common execution-result interface. | Engine-specific schema/load/psql/mysql/spark details. |
| PostgreSQL execution | Current `src/sql_rewrite_bench/postgres_execution.py` | PostgreSQL local schema setup, DDL/load resolution through manifest/external schema metadata, source/candidate execution, local result artifacts, future raw timing samples. | Speedup computation, official metrics, report rendering. |
| MySQL execution | Future `src/sql_rewrite_bench/mysql_execution.py` | MySQL diagnostic execution under the common execution interface. | Official metrics or cross-engine claims. |
| Spark execution | Future `src/sql_rewrite_bench/spark_execution.py` | Spark SQL diagnostic execution under the common execution interface. | Official metrics or cross-engine claims. |
| Local result checker | Current `src/sql_rewrite_bench/local_result_checker.py` | Comparing local source/candidate JSONL result artifacts using case-local checker config; exact/mismatch/checker_failed. | SQL execution, candidate preflight, performance timing, official verifier claims. |
| Ledger/failure bucket writer | Proposed `src/sql_rewrite_bench/user_ledger.py` | Row status consolidation, failure-bucket priority, writing `ledger.csv`, `failures.csv`. | DB execution or metrics. |
| Local quality report | Proposed `src/sql_rewrite_bench/user_quality_report.py` | Denominator-aware local diagnostic summary and `quality_report.md`. | Official metric computation, paper tables, leaderboard. |
| Tag-aware slices | Proposed `src/sql_rewrite_bench/tag_slices.py` | Joining ledger rows with manifest/taxonomy tags and writing `tag_slices.csv`. | Tag score, ranking, leaderboard. |
| Timing diagnostic | Future/deferred `src/sql_rewrite_bench/timing_diagnostic.py` | Exact-only local timing diagnostic design later. | Official paper timing metrics unless separately authorized. |
| User run schema | Current `src/sql_rewrite_bench/user_run_schema.py` | Typed local row/status schema. | DB execution or metric computation. |

## 6. Candidate correctness layers

Candidate correctness must be layered:

- Candidate preflight: SQL text/safety/readiness before DB.
- DB execution: engine actually runs source/candidate.
- Local result checker: compares execution results.
- Formal verifier support: future/support layer, not user-entry default.

`local_result_checker.py` is not a SQL parser, not an executor, not a performance module, and not an official semantic-equivalence verifier. It compares local source/candidate JSONL artifacts under case-local checker/normalization configuration and reports diagnostic exact/mismatch/checker_failed states.

## 7. Engine execution design

Future engine execution should expose a common execution result interface with fields such as:

- `engine`
- `case_id`
- `source_execution_status`
- `candidate_execution_status`
- `schema_setup_status`
- `source_result_path`
- `candidate_result_path`
- `source_error_path`
- `candidate_error_path`
- `execution_artifact_dir`
- `engine_version`, if available
- future timing sample fields, if timing is later enabled

`postgres_execution.py` is the current implementation. `mysql_execution.py` and `spark_execution.py` are future modules. Engine execution may collect raw timing samples later, but must not compute speedup or official metrics.

## 8. Ledger and failure bucket design

Future local ledger funnel:

```text
selected
-> adapter_invoked
-> candidate_generated
-> candidate_preflight_passed
-> db_execution_attempted
-> source_executable
-> candidate_executable
-> checker_attempted
-> exact/mismatch
-> source_like/nontrivial flag
-> timed later
```

Provisional failure bucket priority:

- `selection_failed`
- `adapter_failed`
- `candidate_missing`
- `candidate_preflight_failed`
- `source_execution_failed`
- `candidate_execution_failed`
- `checker_failed`
- `mismatch`
- `source_like_or_noop`
- `none`

A future `repository_spec/user_entry_failure_bucket_policy_v0.md` should formalize this priority before implementation.

## 9. Tag-aware diagnostic design

Tags must be loaded from manifest/taxonomy retained metadata, not guessed from SQL text at runtime. Tag slices are diagnostic slices, not scores. Tag slices must be denominator-aware.

Proposed output:

`runs/user/{run_name}/tag_slices.csv`

Proposed fields:

- `axis`
- `tag`
- `selected_rows`
- `candidate_generated_rows`
- `candidate_preflight_passed_rows`
- `candidate_executed_rows`
- `checker_attempted_rows`
- `exact_rows`
- `mismatch_rows`
- `execution_failed_rows`
- `checker_failed_rows`
- `source_like_or_noop_rows`
- `timed_rows`
- `claim_boundary`

No tag score. No tag-weighted ranking. No leaderboard.

## 10. Local quality report design

Proposed outputs:

- `runs/user/{run_name}/quality_summary.json`
- `runs/user/{run_name}/quality_report.md`

They summarize local diagnostics only:

- selected rows
- generated rows
- preflight rows
- executable rows
- checker attempted rows
- exact rows
- mismatch rows
- failure buckets
- tag slices, if available

They must not be called official metrics.

## 11. Output layout policy

Intended user-run output layout:

```text
runs/user/{run_name}/
  config.yaml
  selected_cases.csv
  candidate_sql/
  workspaces/
  execution/
  checker/
  ledger.csv
  failures.csv
  summary.json
  report.md
  quality_summary.json        # future
  quality_report.md           # future
  tag_slices.csv              # future
```

User runner must not write to:

- `cases/`
- case-local `runs/`
- `case_sets/`
- `reports/`
- `results/`
- `inventory/`
- raw retained evidence

## 12. Timing diagnostic boundary

- Timing is deferred.
- Raw timing should be collected by engine execution modules only when explicitly enabled.
- Speedup interpretation belongs to a report/metrics layer after exactness is known.
- Official timing metrics require separate authorization.
- `GM_Speedup` and `Speedup Ratio Percentiles` are governed by `repository_spec/metrics_contract_v1.md`.
- Performance is only interpretable on exact + timed rows.

## 13. Implementation phases

- U0. Architecture plan in project_control.
- U1. Output schema and ledger-field audit.
- U2. Module split design for resolver / adapter runner / ledger writer.
- U3. Candidate preflight v0.
- U4. Local quality report v0.
- U5. Tag-aware slices v0.
- U6. User readability enhancements: `--list-cases`, `--explain-selection`, `--show-output-schema`.
- U7. Engine execution router and MySQL/Spark fail-closed interface design.
- U8. Timing diagnostic design, deferred until metric/timing protocol approval.
- U9. Paper reproduction / official metrics, separate future phase only.

## 14. Acceptance criteria for this stage

This stage is complete when:

- users can choose Common-core v0 subsets by case/pool/engine
- adapter output is captured
- candidate preflight status is recorded
- optional PostgreSQL DB/checker correctness diagnostic works locally
- local quality summary is denominator-aware
- tag-aware slices explain failure/exactness by labels
- all outputs stay under `runs/user/{run_name}/`
- no official metrics or leaderboard are produced
- docs explain boundaries clearly

## 15. Explicitly deferred work

- official metrics computation
- paper table rendering
- retained-evidence adapter integration
- reports/results migration
- full reproduction CLI
- SpeedupTransferRate
- global leaderboard
- release export/tagging
