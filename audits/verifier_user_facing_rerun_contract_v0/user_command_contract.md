# User Command Contract

Current implemented verifier facade:

```bash
sqlrb user verify --run-id <run_id> --tool sqlsolver --output-root output --pair-scope synthetic-smoke
sqlrb user verify --run-id <run_id> --tool verieql --output-root output --pair-scope synthetic-smoke
```

Current optional flags:

- `--tool-cmd <path-or-command>`
- `--timeout <seconds>`

Current limitation:

- `sqlrb user verify` exposes `run-candidates` and `controls` as future pair-scope choices, but the implementation currently accepts only `synthetic-smoke`.
- `sqlrb user evaluate --verifier ...` is still fail-closed and raises that verifier integration is not implemented.

Required future exact-candidate rerun command shape:

```bash
sqlrb user verify \
  --run-id <verifier_run_id> \
  --tool sqlsolver \
  --output-root output \
  --pair-scope run-candidates \
  --source-run-id <candidate_run_id> \
  --method-id <method_id> \
  --engine <engine> \
  --identity-guard required
```

Equivalent VeriEQL shape:

```bash
sqlrb user verify \
  --run-id <verifier_run_id> \
  --tool verieql \
  --output-root output \
  --pair-scope run-candidates \
  --source-run-id <candidate_run_id> \
  --method-id <method_id> \
  --engine <engine> \
  --identity-guard required \
  --verifier-mode finite_bound \
  --bound-size <n>
```

This target shape is not fully implemented today. The missing gaps are documented in `open_gaps_before_final_rerun.md`.
