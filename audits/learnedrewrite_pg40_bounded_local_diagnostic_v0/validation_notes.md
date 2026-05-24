# Validation Notes

Completed checks:

- `pytest tests/user_entry/test_learnedrewrite_adapter.py -q`: passed, `14 passed, 8 subtests passed`.
- `python -m py_compile baselines/learnedrewrite/adapter.py`: passed.
- Selection check: `python -m cli.main user explain-selection --case-set common_core_v0 --engines postgres` selected exactly 40 rows.
- Evaluate run completed for PostgreSQL only: selected rows = 40.
- compute-local-metrics completed through `python -m cli.main user compute-local-metrics` and wrote local_metrics.py outputs.
- CSV parse checks passed for generated audit CSVs before closeout.
- JSON parse checks passed for generated audit JSON before closeout.
- Markdown/text non-empty checks passed for generated audit Markdown/text files before closeout.
- DB/checker/timing bounded-scope check passed: only PostgreSQL rows were selected.
- MySQL/Spark run check passed: no MySQL or Spark engine was selected.
- Verifier/LLM check passed: no SQLSolver, VeriEQL, R-Bot, LLM-R2, or live LLM command was run.
- Runtime shutdown check passed after evaluate/local_metrics.
- No JAR/source/rules asset copied into the release repo.
- No top-level `reports/` or `results/` update occurred.
- No official metrics, paper rendering, retained evidence promotion, leaderboard, or Track A 120 command occurred.

Checks completed during final closeout:

- Runtime output cleanup from `runs/user/learnedrewrite_pg40_bounded_diagnostic_v0` and `/tmp/sqlrb_learnedrewrite_pg40_bounded_local_diagnostic_v0`.
- No runtime outputs staged.
- Changed-file secret scan.
- Protected-path review.
- `git diff --check`.

Boundary result:

- denominator changed: no
- paper results changed: no
- case membership changed: no
- raw legacy evidence changed: no
