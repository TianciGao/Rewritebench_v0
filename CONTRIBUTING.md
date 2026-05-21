# Contributing

SQL-RewriteBench accepts conservative public-release contributions that do not silently change benchmark meaning.

Welcome contribution types:

- Documentation fixes.
- Adapter examples.
- Typo fixes.
- Issue reports with reproducible context.
- Small packaging or usability fixes that preserve benchmark boundaries.

Contributions must not silently change:

- Common-core membership.
- Denominator definitions.
- Official metrics.
- `reports/` or `results/`.
- Retained evidence.
- `case_sets/`.
- Benchmark claims.

The following changes require maintainer review and explicit policy approval before implementation:

- New cases.
- Metric changes.
- Reports/results updates.
- Retained-evidence changes.
- Denominator changes.
- Case-set changes.
- Benchmark-claim changes.

User-run outputs should not be committed. New local outputs belong under `runs/user/...` and remain local diagnostics unless a separate retained-evidence policy explicitly promotes them.

Do not commit secrets, API keys, local database dumps, local credentials, large generated run outputs, or private machine paths.

SQL-RewriteBench does not provide a global leaderboard. Contributions must not introduce leaderboard claims, rank methods globally, or collapse role-specific and denominator-specific results into a single overall score.
