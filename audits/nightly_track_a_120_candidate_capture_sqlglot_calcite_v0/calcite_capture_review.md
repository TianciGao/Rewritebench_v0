# Calcite Capture Review

Calcite HEP fail-closed was attempted through the existing adapter:

```bash
python baselines/calcite_hep_fail_closed/adapter.py
```

Planned rows: 120. Candidate-present rows: 0.

All 120 rows were `preflight_blocked` because the Calcite external runtime was not configured in this shell. The adapter status was `calcite_runtime_unavailable` with no candidate SQL emitted.

This task did not fabricate Calcite candidates for unsupported, parse-failed, or fail-closed rows. It did not copy candidates from prior local roots.

Per-engine result:

- PostgreSQL: 0/40 candidate-present, 40 preflight-blocked
- MySQL: 0/40 candidate-present, 40 preflight-blocked
- Spark: 0/40 candidate-present, 40 preflight-blocked

Calcite HEP fail-closed therefore produced 120 planned manifest rows and no candidate files in this nightly capture.
