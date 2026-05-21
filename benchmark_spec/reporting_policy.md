# Reporting Policy

SQL-RewriteBench results must be role-aware and denominator-aware.

Reporting boundaries:

- Hard negatives are checker controls, not method-generated candidates.
- Verifier support is not a rewrite-generation baseline.
- `SpeedupTransferRate` is currently not computed for current evidence.
- No global leaderboard is provided.
- User-entry local diagnostics are not official metrics.
- Performance is interpretable only on exact + timed rows.
- PORT bounded evidence must not be described as full PORT9 closure.

Official metrics, paper table rendering, reports/results migration, retained-evidence promotion, timing/speedup computation, denominator changes, paper-result changes, and leaderboard output require separate authorization.
