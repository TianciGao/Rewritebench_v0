# PORT Cross-Dialect MySQL Live Diagnostic

Verdict: `completed_local_diagnostic`.

This packet summarizes a bounded local diagnostic for five Common-core PORT
cross-dialect rows that require MySQL source-reference execution:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

Run output path:

`runs/user/port_mysql_source_reference_live/`

The run used the public no-op adapter. For these PORT rows, the no-op adapter
emits source-like MySQL SQL, so PostgreSQL target-candidate execution was
expected to be a diagnostic target-side failure mode rather than an official
method failure.

## Environment

- PostgreSQL probe result: ok.
- MySQL probe result: ok.
- Spark status: deferred/fail-closed.

## Summary

| Field | Count |
|---|---:|
| Selected rows | 5 |
| MySQL source-reference attempted rows | 5 |
| MySQL source-reference executable rows | 5 |
| MySQL source-reference failed rows | 0 |
| PostgreSQL target-candidate attempted rows | 5 |
| PostgreSQL target-candidate executable rows | 0 |
| PostgreSQL target-candidate failed rows | 5 |
| Checker attempted rows | 0 |
| Checker exact rows | 0 |
| Checker mismatch rows | 0 |

Failure bucket summary:

| Failure bucket | Rows | Related area |
|---|---:|---|
| `candidate_execution_failed` | 5 | target |

Failure classification:

- Connection-related failures: no.
- Config-related failures: no.
- Schema-related failures: no.
- Source-reference failures: no.
- Target-candidate failures: yes, 5 rows.
- Checker-related failures: no.

## Interpretation Boundary

- Local diagnostic only.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Reports/results updated: no.
- Retained evidence updated: no.
- Denominator changed: no.
- Paper results changed: no.
- Global leaderboard created: no.

## Files

- `environment_check.md`: local engine probe result.
- `live_run_summary.json`: machine-readable diagnostic summary.
- `source_reference_execution_summary.csv`: per-row MySQL source-reference outcome.
- `target_candidate_outcome_summary.csv`: per-row PostgreSQL target-candidate outcome.
- `failure_bucket_summary.csv`: failure bucket and related-area classification.
- `artifact_inventory.csv`: run-output artifact inventory by row and artifact type.
- `command_log.md`: commands used for repository state, probes, run, and inspection.
- `protected_surface_check.md`: mutation-boundary and validation checks.
