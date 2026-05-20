# Quality Summary Schema

`quality_summary.json` uses schema version `local_quality_report_v0`.

Top-level fields:

- `schema_version`: local schema identifier.
- `scope`: run scope and boundary flags.
- `funnel_counts`: denominator-aware local diagnostic funnel counts.
- `failure_bucket_counts`: aggregate local diagnostic failure buckets from `ledger.csv`.
- `status_counts`: aggregate local status families from `ledger.csv`.
- `interpretation_boundary`: explicit non-official boundary flags.
- `derivation_notes`: conservative derivation notes for fields that are implicit in the current ledger.

Required `scope` flags:

- `local_diagnostic_only: true`
- `official_metrics: false`
- `paper_results_updated: false`
- `retained_evidence_input: false`
- `leaderboard_created: false`

The schema intentionally excludes official metric names, paper-table fields, retained-evidence inputs, timing/speedup fields, and leaderboard fields.
