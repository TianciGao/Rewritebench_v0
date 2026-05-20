# Risk Register

## `user_run.py` Over-Refactor

Risk: moving orchestration, reporting, DB/checker routing, and future features at once could change public smoke behavior.

Mitigation: extract resolver, adapter runner, and ledger writer in separate behavior-preserving commits. Keep summary/report generation and DB/checker orchestration in `user_run.py` for the minimal split.

## Accidental Smoke Behavior Change

Risk: changes to cwd, `shell=False`, adapter environment variables, candidate capture priority, or output paths could break existing users.

Mitigation: require help, dry-run smoke, adapter-capture smoke, and `tests/user_entry` after each extraction.

## Official Metrics Mixed Into Local Diagnostics

Risk: ledger and quality-report wording could be interpreted as official benchmark metrics.

Mitigation: keep `official_metric_input=false`, `local_execution_only=true`, and explicit no-paper/no-leaderboard boundary flags. Do not add official metric names to user-run outputs.

## Tag Inference From SQL Text

Risk: future tag slices could infer taxonomy from SQL text and drift from manifest metadata.

Mitigation: resolver exposes manifest/taxonomy metadata; tag slices consume resolver-provided tags only.

## Outputs Outside `runs/user/`

Risk: extracted modules could write workspace, candidate, checker, or execution artifacts outside the allowed local user-run root.

Mitigation: output-root validation remains in `user_run.py`; adapter runner and ledger writer receive only validated output directories and ensure per-row paths stay below them.

## DB/Checker Dependency Creep Into Smoke

Risk: resolver or ledger extraction could require DB/checker metadata for the default public smoke path.

Mitigation: resolver should support required-now fields for non-DB smoke and only require DB/checker-specific assets when the corresponding option is enabled.

## Resolver Duplication With PostgreSQL Schema Resolution

Risk: both resolver and `postgres_execution.py` may parse schema metadata differently during transition.

Mitigation: minimal split may leave PostgreSQL schema asset resolution unchanged; a later engine-router task should consolidate shared schema resolution.

## CSV Schema Churn

Risk: adding new fields during module split could break downstream local tooling and existing tests.

Mitigation: preserve current `LEDGER_FIELDS`, `SELECTED_CASE_FIELDS`, and `FAILURE_FIELDS` in minimal implementation. Add U3+ fields only with explicit schema updates and tests.
