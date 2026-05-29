# Calcite HEP Track A 120 Canonical User Rerun With Metrics v0

This packet records the canonical local-only Track A 120 rerun for `calcite_hep_fail_closed`.

The run used the D035 user facade and then computed local diagnostic metrics with `src/sql_rewrite_bench/local_metrics.py` through `python -m cli.main user compute-local-metrics`.

Scope:
- case set: `common_core_v0`
- engines: `postgres,mysql,spark`
- planned rows: 120
- route_id: `calcite_hep_fail_closed`
- method_id: `calcite_hep_fail_closed`
- adapter: `baselines/calcite_hep_fail_closed/adapter.py`
- run id: `calcite_hep_track_a_120_canonical_v0`

Boundary:
- local diagnostic only
- official metric input: false
- paper result input: false
- retained evidence promoted: false
- leaderboard input: false
- Semantic Equivalence Rate: N.A. without verifier evidence
- formal Regression@20: not emitted

Canonical metrics source:
- `runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_summary.json`
- `runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_by_engine.csv`
- `runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_by_pool.csv`
- `runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_timing_speedup_rows.csv`
- `runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_boundary.md`

Copied canonical snapshots:
- `canonical_metrics_snapshot.json`
- `canonical_engine_metrics_snapshot.csv`
