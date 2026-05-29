# SQLGlot Capture Review

## SQLGlot No-Op

SQLGlot no-op was captured through the existing adapter:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route noop
```

Planned rows: 120. Candidate-present rows: 115.

Per-engine candidate-present counts:

- PostgreSQL: 35/40
- MySQL: 40/40
- Spark: 40/40

The five PostgreSQL failures are all `generation_failed` / `sqlglot_parse_failed` rows:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

SQLGlot no-op did not reach 120 candidate-present rows. Missing rows remain manifest-visible.

## SQLGlot Optimize Schema-Aware

SQLGlot optimize schema-aware was captured through the existing schema-aware route:

```bash
python baselines/sqlglot/sqlglot_user_adapter.py --route optimize_schema_aware
```

It was not silently downgraded to no-op or schema-unaware optimize.

Planned rows: 120. Candidate-present rows: 105.

Per-engine candidate-present counts:

- PostgreSQL: 34/40
- MySQL: 32/40
- Spark: 39/40

Frontier rows:

- MySQL generation failures: `CONS_0009`, `CONS_0010`, `CONS_0011`
- MySQL preflight-blocked rows: `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `CONS_0005`
- PostgreSQL generation failures: `CONS_0009`, `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`
- Spark generation failure: `CONS_0009`

SQLGlot optimize schema-aware did not reach 120 candidate-present rows. Missing and blocked rows remain manifest-visible.

## Boundary

Candidate status is artifact status only. It is not correctness, execution status, timing status, POCR, or paper-facing evidence.
