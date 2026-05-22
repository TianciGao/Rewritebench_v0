# Test Plan

## Output Writer Tests

- Path construction creates `output/results/<run_id>`, `output/logs/<run_id>`, and `output/reports/<run_id>`.
- Path validation rejects traversal and accidental top-level `reports/` or `results/` writes.
- `run_manifest.json` contains required schema fields and local-only boundary flags.
- `boundary.md` states local-only, non-official, non-retained, non-leaderboard status.
- Failure bucket CSV and Markdown are derived from current failure/ledger artifacts.
- Tag-slice CSV and Markdown placement matches the contract.
- Timing and metrics directories are copied only when source artifacts exist.
- Verifier placeholders stay N.A. until formal integration exists.
- Output writer does not change `runs/user/` contents except through the existing runner.

## CLI Facade Tests

- `sqlrb user evaluate --help` parses.
- `sqlrb user list-cases` delegates to metadata-driven selection.
- `sqlrb user explain-selection` delegates to existing selection explanation.
- `sqlrb user show-output-schema` describes the D035 output contract.
- `sqlrb user evaluate` bounded smoke invokes the existing internal runner and output writer.
- `sqlrb user compute-local-metrics` delegates to local metrics code without route mixing.
- `sqlrb user summarize` reads output artifacts without recomputing metrics by default.
- `sqlrb user show-boundary` renders or prints local-only boundary text.

## Regression Guards

- No writes to top-level `reports/` or `results/`.
- No `output/` runtime artifacts staged or committed.
- No source/checker/exactness behavior change.
- No timing collection unless explicitly requested.
- No official metrics, paper tables, retained evidence, or leaderboard artifacts.
- `runs/user/` transition compatibility is preserved.
