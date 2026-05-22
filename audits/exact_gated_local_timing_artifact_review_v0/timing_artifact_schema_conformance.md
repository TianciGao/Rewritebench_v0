# Timing Artifact Schema Conformance

## Scope

Reviewed existing bounded SQLGlot noop timing smoke artifacts for PostgreSQL, MySQL, and Spark:

- `runs/user/timing_sqlglot_noop_postgres_smoke/timing/`
- `runs/user/timing_sqlglot_noop_mysql_smoke/timing/`
- `runs/user/timing_sqlglot_noop_spark_smoke/timing/`

No timing rerun was performed.

## Required Files

All three reviewed run directories contain:

- `timing_policy.json`
- `environment_metadata.json`
- `timing_summary.json`
- `timing/rows/*.json`

Each run has two timing row artifacts, one for `PERF_0006` and one for `CONS_0005`.

## Policy Artifacts

Observed `timing_policy.json` schema:

- `schema_version=timing_policy_schema_v0`
- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

## Environment Artifacts

Observed `environment_metadata.json` schema:

- `schema_version=timing_environment_metadata_v0`
- local-only claim boundary present
- no secret dump or full environment dump recorded

## Summary Artifacts

Observed `timing_summary.json` schema:

- `schema_version=local_timing_summary_v0`
- selected row and timing status counts are local diagnostic summaries only
- local-only claim boundary fields are present

## Row Artifacts

All six row artifacts contain the required identity, exactness, timing, SQL hash, artifact path, and claim-boundary fields listed in the v0 draft schema and this task.

No schema gaps were found in the reviewed bounded smoke artifacts.
