# Validation Notes

Validation results:

- CSV parse checks: passed for 5 CSV files.
- Markdown non-empty checks: passed for 8 Markdown files.
- Source audit existence checks: passed for 15 source paths used by the packet.
- Copied metric value checks: passed for representative canonical metric tokens copied from the existing unified evidence summary and local_metrics review files.
- Exact paper metric-name check: passed for all required names:
  - Generation Rate
  - Execution Coverage Rate
  - Result Consistency Rate
  - Semantic Equivalence Rate
  - GM Speedup Ratio
  - Speedup Ratio Percentiles
  - Positive Operation Coverage Rate
  - Cross-Engine Execution Coverage Rate
  - Cross-Engine Result Consistency Rate
  - Cross-Engine GM Speedup Ratio
- Forbidden abbreviation-only metric column check: passed; no abbreviation-only metric column appears.
- All Track A 120 route representation check: passed for Direct LLM original, Direct LLM + Repair-1, SQLGlot no-op, SQLGlot optimize schema-aware, and Calcite HEP fail-closed.
- All three PG40 prior-method representation check: passed for LearnedRewrite, R-Bot adapted GPT-5.4, and LLM-R2 adapted GPT-5.4.
- No-prohibited-command check: passed for executable command lines recorded in `command_log.txt`.
- `git diff --check`: passed.
- Changed-file secret scan: passed for the new packet and project-control files.
- Protected-path review: passed; changed files are limited to `audits/paper_facing_result_tables_v0/`, `project_control/MIGRATION_STATUS.md`, and `project_control/MIGRATION_RUN_LOG.md`.

Boundary checks:

- No experiment, baseline, live LLM call, DB execution, checker execution, timing collection, local metric computation, SQLSolver, VeriEQL, official metric generation, paper rendering, retained-evidence promotion, leaderboard generation, or Track A 120 command occurred.
- No top-level `reports/` or `results/` update occurred.
- No retained evidence or paper result file was modified.
