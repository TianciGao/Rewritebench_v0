# Command Examples

List all Common-core cases from case-set metadata:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases
```

List PERF cases:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --pool PERF --list-cases
```

Explain the deterministic smoke selection:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --explain-selection
```

Show local output schemas:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema
```

These commands are local transparency helpers. They do not compute official
metrics, render paper tables, update reports/results, parse retained evidence,
or create leaderboard output.
