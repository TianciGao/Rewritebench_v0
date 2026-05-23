# Recommended Candidate Cases

## First Candidate

`CONS_0007` remains the strongest first bounded verifier-support candidate found in the baseline smoke readiness path.

Reasons:

- It was the only `support_candidate` in `sqlsolver_verieql_support_readiness_v0.json`.
- It is a compact Calcite-derived consistency case.
- It has source, positive rewrite, negative rewrite, and PostgreSQL DDL in the legacy case package.
- It directly supports `source_vs_positive` and `source_vs_hard_negative` style verifier pairs.
- It is useful as support/verifier evidence and hard-negative control evidence, not as rewrite generation or speedup evidence.

## Secondary Candidate

`CONS_0035` appears in adjacent legacy scratch notes and historical VeriEQL/SQLSolver support outputs outside `reports/baseline_smoke/`.

Use it only as a secondary canary candidate because the legacy notes show constraint-sensitive behavior:

- SQLSolver historical support smoke produced one unexpected positive-pair verdict on `CONS_0035`.
- VeriEQL historical canary refuted the positive pair under empty constraints and timed out under a uniqueness constraint bridge.

## Later Candidates

The readiness artifact marked these as `maybe`:

- `PERF_0006`
- `PERF_0008`
- `PERF_0024`
- `PERF_0033`
- `PERF_0054`
- `CONS_0012`

They should not be first. Analytical PERF rows require aggregate/bag-semantics support confirmation. `CONS_0012` carries LIMIT/OFFSET and correlation risk.

## Excluded First-Scaffold Cases

The readiness artifact excluded:

- `PERF_0013`
- `PERF_0017`

Reason: interval/date semantics raise symbolic encoding risk for first SQLSolver/VeriEQL support scaffolding.
