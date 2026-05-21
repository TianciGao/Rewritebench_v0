# Future Fix Prompt

Task title: Design and implement narrow PORT reverse cross-dialect MySQL diagnostic routing for `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`

Purpose: The MySQL same-engine local diagnostic triage found that these four PORT cases have PostgreSQL-like `sql/source.sql` files and legacy evidence that compares PostgreSQL source reference output to MySQL positive target output. The current `--engine mysql` same-engine route executes `source.sql` directly in MySQL and fails with syntax errors.

Requirements:

- Review the current `local_diagnostic` metadata for the four cases and decide whether explicit reverse cross-dialect metadata is needed.
- Preserve existing same-engine behavior for PERF, CONS, LONGTAIL, and true same-engine PORT rows.
- Preserve the existing MySQL-source to PostgreSQL-target path for `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- Do not edit SQL files unless a separate maintainer decision explicitly authorizes case-package changes.
- Do not compute official metrics, timing, speedup, reports/results updates, paper tables, denominator changes, retained-evidence promotion, or leaderboard outputs.
- Add tests that prove unsupported or ambiguous routes fail closed.

Expected output: a narrow audit and, only if authorized, a minimal metadata/runner fix that distinguishes legacy PostgreSQL-source to MySQL-target validation from MySQL same-engine source execution.
