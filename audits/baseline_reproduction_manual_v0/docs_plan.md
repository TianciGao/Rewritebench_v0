# Documentation Plan

Goal: create a user-facing baseline reproduction manual for local diagnostic reproduction paths across deterministic, LLM, prior-method, control, and verifier-support routes.

Documentation placement:

- Main manual: `docs/baseline_reproduction.md`
- Example pointer: `examples/baseline_reproduction/README.md`
- Top-level index: `README.md`
- Docs index: `docs/README.md`
- Examples index: `examples/README.md`

The manual documents:

- first-time setup from a fresh checkout;
- CLI entrypoint alternatives: `sqlrb user ...` and `PYTHONPATH=src python -m cli.main user ...`;
- D035 user-output roots;
- smoke commands that do not require DB engines;
- preflight checks for Python, SQLGlot, PostgreSQL, MySQL, Spark, Java, and Calcite;
- canonical timing policy;
- baseline-specific command patterns and boundaries;
- POCR relationship and diagnostic-only boundary;
- troubleshooting guidance.

The manual intentionally does not run or authorize any baseline, DB/checker/timing pass, LLM/API call, POCR annotation generation, official metric computation, paper table update, retained-evidence promotion, or leaderboard output.
