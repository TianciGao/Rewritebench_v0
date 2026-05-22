# Phase 2 Implementation Slices

## Phase 2A: Output Writer Skeleton

Implement:

- `src/sql_rewrite_bench/user_output.py`
- output root/path validation for `output/results/<run_id>`, `output/logs/<run_id>`, and `output/reports/<run_id>`
- `run_manifest.json`
- `boundary.md`
- export of existing bounded-smoke artifacts from `runs/user/<run_id>/` into the output contract
- failure bucket CSV/Markdown generation from current ledger/failure files
- tag-slice Markdown generation from current `tag_slices.csv`

Do not implement:

- public CLI facade
- verifier execution
- official output promotion
- paper reports/results updates
- leaderboard output

Validation target:

- bounded SQLGlot noop smoke only
- no top-level `reports/` or `results/` changes
- output runtime artifacts ignored/uncommitted

## Phase 2B: CLI Facade Core

Implement:

- `src/cli` package
- `sqlrb user evaluate`
- `sqlrb user list-cases`
- `sqlrb user explain-selection`
- `sqlrb user show-output-schema`
- CLI parsing tests
- bounded SQLGlot noop smoke through the facade

Implementation rule:

- `src/cli` delegates to `src/sql_rewrite_bench`; it does not duplicate business logic.

## Phase 2C: Metrics and Summary Facade

Implement:

- `sqlrb user compute-local-metrics`
- `sqlrb user summarize`
- `sqlrb user show-boundary`
- output-compatible local metrics placement under `output/results/<run_id>/metrics/`
- `output/reports/<run_id>/metrics_summary.md`

Still deferred:

- VeriEQL and SQLSolver execution
- official metrics
- retained-evidence promotion
- paper table rendering
- leaderboard output
