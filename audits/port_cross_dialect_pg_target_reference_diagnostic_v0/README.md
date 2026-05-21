# PORT Cross-Dialect PostgreSQL Target-Reference Diagnostic

Verdict: `completed_local_diagnostic_with_checker_mismatches`.

This packet summarizes a bounded local diagnostic for five Common-core PORT cross-dialect rows:

- `PORT_0004`
- `PORT_0013`
- `PORT_0022`
- `PORT_0024`
- `PORT_0025`

Run output path:

`runs/user/port_pg_target_reference_controlled/`

The run used `examples/user/port_postgres_target_reference_adapter.py`, a controlled diagnostic adapter that copies only the manifest-declared `local_diagnostic.target_reference.query` into the runner-provided candidate path. The adapter is not a user method, not a benchmark baseline, and not a source oracle.

## Environment

- PostgreSQL probe result: ok.
- MySQL probe result: ok.
- Spark status: deferred/fail-closed.

## Summary

| Field | Count |
|---|---:|
| Selected rows | 5 |
| Candidate generated rows | 5 |
| MySQL source-reference attempted rows | 5 |
| MySQL source-reference executable rows | 5 |
| MySQL source-reference failed rows | 0 |
| PostgreSQL target-candidate attempted rows | 5 |
| PostgreSQL target-candidate executable rows | 5 |
| PostgreSQL target-candidate failed rows | 0 |
| Checker attempted rows | 5 |
| Exact rows | 1 |
| Mismatch rows | 4 |

Failure bucket summary:

| Failure bucket | Rows | Related area |
|---|---:|---|
| `mismatch` | 4 | checker/normalization comparison |
| `none` | 1 | none |

Failure classification:

- Source-reference failures: no.
- Target-candidate execution failures: no.
- Schema failures: no.
- Checker/normalization mismatches: yes, 4 rows.

## Interpretation Boundary

- Local diagnostic only.
- Controlled adapter is not a user method or benchmark baseline.
- `pos_01.sql` remains a manifest-declared positive target reference, not a source oracle.
- Official metrics computed: no.
- Timing/speedup computed: no.
- Reports/results updated: no.
- Retained evidence updated: no.
- Denominator changed: no.
- Paper results changed: no.
- Global leaderboard created: no.
