# Transition Strategy: runs/user to output

## Current State

`runs/user/<run_id>/` is the current local diagnostic work surface. It is already used by user-run execution, timing artifacts, and non-official local metrics.

## Future User-Facing State

D035 sets the future public output contract:

```text
output/results/<run_id>/
output/logs/<run_id>/
output/reports/<run_id>/
```

## Transition Plan

1. Preserve `runs/user/` during Phase 2A and Phase 2B.
2. Add `output/` export as a user-facing layer.
3. Do not delete or move existing `runs/user/` outputs.
4. Do not write to top-level `reports/` or `results/`.
5. Keep output runtime artifacts ignored/uncommitted.
6. Use `run_manifest.json` to record both legacy/dev roots and user-facing output roots during the transition.
7. Once CLI and output writer are stable, consider whether `runs/user/` remains developer-only or becomes an internal staging detail.

## Compatibility Expectations

- Existing internal commands should keep working.
- Existing local metrics calculator should continue to accept `runs/user/<run_id>/` until an output-aware wrapper is implemented.
- New public commands should prefer `--output-root output`.
- Audit packets may summarize output files but must not commit runtime output directories.
