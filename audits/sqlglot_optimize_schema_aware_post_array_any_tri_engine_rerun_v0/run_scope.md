# Run Scope

This rerun covered only the bounded tri-engine smoke scope used by the prior schema-aware SQLGlot optimize diagnostics.

## Route

- `method_id`: `sqlglot`
- `route_id`: `sqlglot_optimize_schema_aware`
- adapter option: `--route optimize_schema_aware`

## Rows

Planned rows: 9.

Cases:

- `CONS_0005`
- `PERF_0006`
- `CONS_0036`

Engines:

- `postgres`
- `mysql`
- `spark`

## Runtime

Runtime artifacts were written under:

- `/tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/`

The committed audit packet contains summaries and ledgers only. It does not contain runtime DB output, user-run output, retained evidence, or official report/result artifacts.

## Exclusions

Not run:

- full Track A 120
- all Common-core rows
- timing
- verifier passes
- SQLGlot noop
- Calcite
- Direct LLM
- Repair-1
- official metrics
- Semantic Equivalence Rate
- formal Regression@20
