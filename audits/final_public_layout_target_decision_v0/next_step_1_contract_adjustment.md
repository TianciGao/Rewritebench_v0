# Step 1 Contract Adjustment

D034 Step 1 is still the next safe action, but D035 adjusts the intended output shape.

## Superseded Shape

```text
output/<run_id>/
  results/
  logs/
  reports/
```

## D035 Target Shape

```text
output/
  results/<run_id>/
  logs/<run_id>/
  reports/<run_id>/
```

## CLI Location

D034 allowed a thin interface under `src/user/` or an equivalent public CLI wrapper. D035 narrows the preferred location:

- public-facing CLI/facade: `src/cli/`
- internal implementation package: `src/sql_rewrite_bench/`
- development and validation tools: `src/dev/`

Step 1 should produce an output/CLI contract that follows these locations without implementing the writer or CLI.
