# Spark Statement Boundary Comment-Aware Patch

Verdict: `completed`.

This patch fixes the narrow Spark local diagnostic statement-boundary gap identified in `spark_sqlglot_noop_statement_preflight_triage_v0`.

## Root Cause Addressed

The prior triage found that SQLGlot noop emitted one SQL query preceded by `/* ... */` block comments. Those comments preserved metadata/provenance semicolons. Candidate preflight already ignored semicolons inside line comments, block comments, and quoted text, so the candidates passed preflight. The Spark local diagnostic backend used a separate splitter that stripped only full-line `--` comments and split on semicolons inside block comments, so the backend rejected the candidates as not exactly one statement.

## Patch Summary

- Added a shared comment-aware SQL statement splitter in `src/sql_rewrite_bench/candidate_preflight.py`.
- Updated candidate preflight multi-statement detection to use that splitter.
- Updated Spark local diagnostic statement splitting in `src/sql_rewrite_bench/spark_execution.py` to reuse the shared splitter after preserving Spark's existing full-line `--` comment normalization.
- Added focused user-entry tests covering semicolons in block comments, line comments, string literals, double-quoted identifiers, backtick identifiers, and genuine multi-statement rejection.

The patch does not change SQLGlot adapter behavior, checker normalization, case packages, SQL files, manifests, schema files, validation scripts, reports/results, retained evidence, or any official metric surface.

## Local Diagnostic Results

Targeted affected-row rerun:

- Run path: `runs/user/spark_sqlglot_noop_statement_boundary_after_patch`
- Selected rows: 6
- Candidate generated rows: 6
- Candidate preflight passed rows: 6
- Source executable rows: 6
- Candidate executable rows: 6
- Checker attempted rows: 6
- Exact rows: 6
- Mismatch rows: 0

Spark two-case smoke:

- Run path: `runs/user/spark_sqlglot_noop_two_case_smoke_after_statement_patch`
- Cases: `PERF_0006`, `CONS_0005`
- Selected rows: 2
- Candidate generated rows: 2
- Source executable rows: 2
- Candidate executable rows: 2
- Checker attempted rows: 2
- Exact rows: 2
- Mismatch rows: 0

These are local diagnostic results only and are not official metrics or paper evidence.

## Boundary

No full Common-core rerun was performed. SQLGlot optimize was not run. Timing/speedup, official metrics, paper rendering, reports/results updates, retained-evidence promotion, release/export/tag creation, and leaderboard output were not performed.

## Next Safe Action

If desired, run a separately authorized Common-core Spark SQLGlot noop local diagnostic snapshot to confirm the broader Spark snapshot moves the six same-engine rows from candidate execution failure to checker outcomes while keeping PORT real-adapter and unsupported/fail-closed rows separate.
