# PG40 Metric Boundary

Source for copied values: `audits/rbot_gpt54_pg40_bounded_local_diagnostic_rerun_with_metrics_v0/local_metrics_summary_review.md`, which states the values are copied from `local_metrics.py` outputs.

Canonical local diagnostic values:

- selected: `40`
- generated: `40`
- candidate_executable: `38`
- exact: `37`
- timed: `33`
- mismatch: `1`
- candidate_execution_failed: `2`
- generation rate: `1.0`
- execution coverage: `0.95`
- result consistency: `0.925`
- GM speedup: `0.9777997901126648`
- P10/P25/P50/P75/P90: `0.5865455274023522` / `0.9845480112740764` / `0.9998615395796396` / `1.0142327268706417` / `1.5983027547333224`

Boundary:

- PostgreSQL-only PG40 local diagnostic only.
- Not Track A 120.
- Not official metrics.
- Not paper results.
- Not retained evidence promotion.
- Not leaderboard input.
- No official SER; SER status is not applicable because formal verifier evidence is missing.
- POCR remains not applicable/deferred and is not inferred from source-like diagnostics.
