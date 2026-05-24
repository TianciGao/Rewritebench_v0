# Next Steps

Recommended next safe action:

Create a canonical local-only route comparison packet using the canonical metrics outputs for:
- `sqlglot_noop_track_a_120_canonical_v0`
- `sqlglot_optimize_schema_aware_track_a_120_canonical_v0`
- `calcite_hep_track_a_120_canonical_v0`

Comparison rules:
- use `local_metrics.py` outputs only
- do not recompute metrics in audit helpers
- keep denominator and timing denominators visible
- do not declare a winner or leaderboard
- do not update paper reports/results

Potential follow-up blocker work remains separate:
- Calcite PORT no-candidate/source-role coverage
- Calcite mismatch triage
- Calcite candidate execution failures
- label-only mismatch policy, if separately authorized
- verifier rerun support, if separately authorized
