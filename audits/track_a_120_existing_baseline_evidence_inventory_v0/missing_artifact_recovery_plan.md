# Missing Artifact Recovery Plan

This inventory reviewed existing canonical Track A 120 aggregate runs and their per-engine source runs only. No rerun or reprocessing was performed.

## Already Present

For all four canonical routes:

- `local_metrics_summary.json`
- `local_metrics_by_engine.csv`
- `local_metrics_by_pool.csv`
- `local_timing_speedup_rows.csv`
- `local_metrics_boundary.md`
- aggregate `ledger.csv`
- per-engine source-run `ledger.csv`
- per-engine source-run `failures.csv`
- per-engine source-run `tag_slices.csv`
- per-engine source-run `candidate_sql/*.sql` for generated candidates
- audit snapshot JSON/CSV/MD files

These are sufficient for metric-summary inventory, failure-bucket inventory, tag-slice presence inventory, and exact-row verifier-pair eligibility inventory.

## Recoverable From Audit Snapshot

- Canonical overall metrics and per-engine metric snapshots are recoverable from audit packet files for each route.
- Direct LLM original per-row metadata is additionally recoverable from its audit snapshot.

## Recoverable From Local Run Ledger

- Failure frontier details can be recovered from aggregate/source ledgers and per-engine `failures.csv`.
- Exact-row candidate paths, execution/checker status, and timing artifact references can be recovered from ledgers.
- Source SQL paths and case paths are recoverable from per-engine `selected_cases.csv`.

## Recoverable By Reprocessing Only, No Adapter Rerun

- A route-level combined tag-failure slice table could be built by joining existing per-engine `tag_slices.csv` with source-run ledgers and manifests.
- A verifier-pair manifest could be generated from exact rows using existing source SQL paths, candidate SQL paths, engine fields, and schema profile references.

## Requires Deterministic Rerun

- None identified for the requested inventory.

## Requires Live LLM Rerun, Avoid Unless Separately Authorized

- None required for inventory.
- Direct LLM candidate SQL is already present for generated rows.

## Unavailable

- Formal verifier outputs are unavailable for all four routes.
- Official SER is unavailable.
- POCR evidence is unavailable because external operation-atom/skill-adapter evidence is deferred.
