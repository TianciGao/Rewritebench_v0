# Result Artifact Contract

Machine-readable run artifacts live under `output/results/<run_id>/`.

## Top-Level Files

- `run_manifest.json`: run identity, configuration, selected denominator, route/method identity, output roots, and boundary flags.
- `ledger.csv`: row-grained status ledger.
- `quality_summary.json`: local diagnostic summary.
- `failure_buckets.csv`: failure bucket summary.
- `tag_slices.csv`: taxonomy/tag-sliced diagnostic summary.

## Directories

- `candidates/`: emitted candidate SQL and adapter metadata.
- `execution/`: source/reference and candidate DB execution artifacts.
- `checker/`: checker details, mismatch artifacts, strict label diagnostics, and label-only diagnostics.
- `timing/`: exact-gated local timing artifacts when timing is enabled.
- `metrics/`: non-official local metrics when explicitly computed.
- `verifier/`: future VeriEQL and SQLSolver support outputs.

## Status Boundary

Result artifacts are local diagnostic outputs. They are not official metrics, paper results, retained evidence, or leaderboard inputs.

Existing exact/mismatch semantics remain unchanged. Label-only mismatches remain mismatches under the strict label policy unless a future case/role/config-gated policy is separately authorized.
