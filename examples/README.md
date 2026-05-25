# Examples

This directory contains public examples for local SQL-RewriteBench user runs.

- `examples/user/noop_adapter.py`: minimal adapter that copies source SQL to
  the candidate path.
- `examples/user/port_*_target_reference_adapter.py`: local diagnostic
  target-reference examples for PORT workflows.
- `examples/pocr_diagnostic/README.md`: optional default-off POCR diagnostic
  command examples for annotation-missing and annotation JSONL replay modes.

Run examples through the D035 user-facing facade:

```bash
PYTHONPATH=src python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres \
  --smoke \
  --adapter-command "python examples/user/noop_adapter.py" \
  --output-root output \
  --run-id example_noop_smoke
```

Exported output belongs under `output/results/<run_id>/`,
`output/logs/<run_id>/`, and `output/reports/<run_id>/`. The current
implementation may create `runs/user/<run_id>/` as internal transitional
staging before export; do not treat that path as the public output contract.
