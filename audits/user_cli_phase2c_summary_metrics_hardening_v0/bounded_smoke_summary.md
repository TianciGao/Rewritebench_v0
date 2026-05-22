# Bounded Smoke Summary

Smoke type: temp-output fixture only.

No Common-core run was performed. No SQLGlot adapter was invoked. No local metrics calculator was run against real run artifacts.

Commands exercised:

```bash
PYTHONPATH=src python -m cli.main user summarize --output-root /tmp/<temp>/output --run-id demo
PYTHONPATH=src python -m cli.main user show-boundary --output-root /tmp/<temp>/output --run-id demo
```

Fixture contents:

- `output/reports/demo/summary.md`
- `output/reports/demo/failure_buckets.md`
- `output/reports/demo/tag_slices.md`
- `output/reports/demo/metrics_summary.md`
- `output/reports/demo/verifier_summary.md`
- `output/reports/demo/boundary.md`

Observed result:

- `summarize` printed output roots, run summary, failure buckets, tag slices, local metrics, verifier, and boundary sections.
- Semantic Equivalence Rate remained `N.A.`.
- POCR remained deferred.
- `show-boundary` printed the local-only boundary.

The temporary fixture was removed after the smoke. No repository `output/` runtime artifacts were created or committed.
