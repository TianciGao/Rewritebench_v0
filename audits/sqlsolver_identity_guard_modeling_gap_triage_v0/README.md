# SQLSolver Identity Guard Modeling-Gap Triage

Task: `sqlsolver_identity_guard_modeling_gap_triage_v0`

This audit-only packet reviews the five identity-guard `unknown` rows from `audits/sqlsolver_bounded_verifier_pass_sqlglot_noop_pg_v0/`.

## Bounded Pass Result Reviewed

- Selected pairs: `8`
- Identity guard passed pairs: `3`
- Identity guard unknown/failed pairs: `5`
- Actual source-candidate checks attempted: `3`
- Actual source-candidate verdicts: `equivalent=3`, `non_equivalent=0`
- `bounded_SER_if_decidable=1.0` over `3` decidable actual checks, local diagnostic support only
- `SER_status=coverage_limited`
- `official_SER=false`

## Unknown Identity Guard Rows

- `LONGTAIL_0011`: unknown/unknown (unsupported_sql_feature)
- `PERF_0006`: unknown/equivalent (wrapper_input_format_gap)
- `PERF_0007`: unknown/unknown (unsupported_postgres_dialect)
- `PORT_0003`: unknown/unknown (schema_canonicalization_gap)
- `PORT_0005`: unknown/unknown (unsupported_postgres_dialect)

## Main Suspected Modeling Gaps

- `schema_canonicalization_gap`: 1
- `unsupported_postgres_dialect`: 2
- `unsupported_sql_feature`: 1
- `wrapper_input_format_gap`: 1

The dominant blocker is not source-candidate disagreement. It is that SQLSolver could not prove identity for several source or candidate inputs, which blocks safe interpretation of those rows as verifier evidence.

## Broader Pass Readiness Verdict

`ready_for_larger_sqlsolver_pass: no`

The full SQLGlot no-op PostgreSQL exact subset and the broader 346-pair manifest remain blocked until wrapper/schema canonicalization and feature-support policy are designed and tested with smaller identity canaries.

## Next Safe Action

Create a narrow SQLSolver wrapper/schema canonicalization design packet. Do not authorize a larger SQLSolver pass, do not run Repair-1, and do not promote SER.
