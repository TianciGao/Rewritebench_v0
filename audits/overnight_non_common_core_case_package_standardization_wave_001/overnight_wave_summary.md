# Overnight Non-Common-core Case Package Standardization Wave 001

## Purpose And Scope

This wave standardized a bounded set of low-risk non-Common-core case packages into canonical release layout. It did not update `case_sets/`, reports, results, denominators, paper results, metrics, or raw legacy evidence.

## Selection Policy

The queue was built from existing governance and staged/backlog preview artifacts. Common-core cases, manual-review cases, orphan/unregistered cases, already migrated cases, and cases with static prompt/API/key, raw-log/debug, local-path, or retained-runs hygiene risk were excluded from migration attempts.

## Completed Cases

- PORT_0002 (PORT)
- PERF_0029 (PERF)

## Deferred Cases

28 considered cases were deferred because static governance flagged local-path, raw-log/debug, retained-runs, or public hygiene risk. They are listed in `overnight_wave_deferred_cases.csv`.

## Skipped Cases

No additional cases were skipped outside the deferred dossier set.

## Pool Counts

Completed pool coverage: PORT=1, PERF=1. Deferred pool coverage is recorded in `overnight_wave_deferred_cases.csv`.

## Hygiene Findings

No raw legacy `runs/` directories were copied. No raw stdout/stderr/debug logs, prompt/API/key traces, raw local-path Spark plans, reports, results, or timing artifacts were copied. PERF_0029 retained PostgreSQL legacy validation scripts with an output-policy caveat; they were not run.

## Validation Results

Static validation results are recorded in `overnight_wave_validation_results.csv`. Command validation was run after package creation.

## Denominator And Paper-result Impact

Common-core membership did not change. `case_sets/` did not change. Denominator values did not change. Paper results did not change. Metrics were not computed and paper tables were not rendered.

## Next Safe Action

Review wave 001 completed packages and deferred hygiene dossiers; decide whether to run `overnight_non_common_core_case_package_standardization_wave_002` or separately authorize staged/backlog membership governance without changing Common-core v0.
