# User Quickstart

This page shows the current D035-shaped local user workflow. It is for local
diagnostic work only. It does not compute official metrics, update paper
results, promote retained evidence, or create leaderboard output.

## Output Contract

User-facing output is exported to:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

The current implementation also stages source-run artifacts under
`runs/user/<run_id>/` before export. That staging path is internal transitional
workspace, not the public output contract.

## Run A Smoke

From a checkout without installation:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_noop
```

After editable install, the same facade is available as:

```bash
sqlrb user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id smoke_noop
```

## Inspect Before Running

```bash
PYTHONPATH=src python -m cli.main user list-cases --case-set common_core_v0 --engines postgres
PYTHONPATH=src python -m cli.main user explain-selection --case-set common_core_v0 --engines postgres --smoke
PYTHONPATH=src python -m cli.main user show-output-schema
PYTHONPATH=src python -m cli.main user show-boundary --output-root output --run-id smoke_noop
```

These commands do not run adapters or update official surfaces.

## Layout Boundaries

- Public CLI facade: `src/cli/`.
- Core implementation: `src/sql_rewrite_bench/`.
- Route-specific baseline adapters: `baselines/`.
- Public examples: `examples/`.
- Current benchmark data paths: `cases/`, `case_sets/`, `schemas/`, and `inventory/`.

The final D035 public layout targets `benchmarks/` for benchmark data, but that
physical migration is deferred until a separate authorized task.
