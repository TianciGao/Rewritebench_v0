# Deferred Work Register

## Engine Execution

- Live MySQL execution is deferred.
- Live Spark execution is deferred.
- MySQL/Spark currently fail closed and do not fall back to PostgreSQL.
- Cross-engine execution or consistency claims remain unauthorized.

## Timing / Performance

- Timing diagnostics are deferred.
- Speedup computation is deferred.
- Performance interpretation remains exact + timed only.
- Warmup, repetition, timeout, cache, and environment policy are not yet approved.

## Official Metrics

- Official metrics remain unauthorized for user-entry outputs.
- User-entry outputs are not official metric inputs.
- SpeedupTransferRate remains deferred.

## Paper Reproduction

- Paper table rendering is deferred.
- Full paper reproduction CLI is deferred.
- User-entry smoke is not paper reproduction.

## Retained Evidence

- Retained-evidence adapter integration is deferred.
- User-run outputs are not retained evidence.
- No raw legacy evidence is modified or promoted.

## Release Surface

- Release-surface metadata work remains separate from user-entry U0-U7.
- LICENSE, CITATION, CONTRIBUTING, benchmark specs, curated reports/results policy, export branch, and release tag readiness should remain separately controlled.

## Post-Release Backlog

- Live MySQL and Spark diagnostics.
- Timing diagnostics and exact-only performance summaries.
- Full reproduction workflows.
- Any official metrics implementation.
- Any public paper renderer.
- Any retained-evidence adapter flow.
- Any global leaderboard remains prohibited.
