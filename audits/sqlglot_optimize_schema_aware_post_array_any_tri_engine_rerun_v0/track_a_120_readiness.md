# Track A 120 Readiness

`sqlglot_optimize_schema_aware` is improved but still not ready for a full Track A 120 local diagnostic rerun.

## Ready

The route is ready for exact-gated timing over the current bounded exact rows if a narrow timing smoke is authorized.

Current exact rows:

- PostgreSQL: `CONS_0005`, `PERF_0006`, `CONS_0036`
- MySQL: `PERF_0006`, `CONS_0036`
- Spark: `PERF_0006`

## Still Blocked

Full 40 x 3 local diagnostic readiness remains blocked by:

- Spark `CONS_0005` semantic mismatch candidate;
- Spark `CONS_0036` label-only mismatch candidate requiring separate policy authorization;
- MySQL `CONS_0005` now classified correctly as fail-closed, but still not an executable exact row;
- current evidence remains a bounded 9-row smoke, not all Common-core evidence.

## Boundary

No official metrics, Semantic Equivalence Rate, paper-facing evidence, retained-evidence promotion, or leaderboard output are authorized by this packet.

Recommended next task:

- run exact-gated timing only over the six current exact rows, or authorize a separate Spark mismatch and label-policy task before any larger 40 x 3 trial.
