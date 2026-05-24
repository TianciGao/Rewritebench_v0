# Metadata Review

The two facade-selected rows wrote `learnedrewrite_status.json` under their per-row workspaces.

## Required Fields Confirmed

Both rows recorded:

- `route_id=learnedrewrite`
- `method_id=learnedrewrite`
- `runtime_mode=fake`
- `fake_runtime=true`
- `external_runtime_configured=false`
- `java_runtime_invoked=false`
- `network_invoked=false`
- `db_execution_invoked=false`
- `checker_invoked=false`
- `timing_invoked=false`
- `local_metrics_invoked=false`
- `verifier_invoked=false`
- `local_diagnostic_only=true`
- `no_upstream_source_or_jar_vendored=true`

Candidate metadata:

- `candidate_generated=true`
- `extraction_status=extracted`
- `failure_bucket=none`
- `candidate_sql_sha256=f71239670681bed98da4045befc8a9a5ecd08f09804b9df5f807af0be9077449`

## Secret Safety

The metadata scan found no secret-like fields or API-key values. No API key was required for this fake runtime smoke.

## Runtime Boundary

The source run ledger recorded `execution_enabled=false`, `checker_enabled=false`, and `timing_status=not_requested` for both rows. The exported user output included the normal verifier placeholder, but no verifier command was run.
