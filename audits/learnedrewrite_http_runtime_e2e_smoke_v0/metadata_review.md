# Metadata Review

Adapter metadata was written to:

```text
runs/user/learnedrewrite_http_runtime_e2e_smoke_v0/workspaces/CONS_0036/postgres/learnedrewrite_status.json
```

Reviewed fields:

- `route_id=learnedrewrite`
- `method_id=learnedrewrite`
- `adapter_version=learnedrewrite_adapter_http_v0`
- `runtime_mode=http`
- `runtime_allow_gate=true`
- `external_http_url_configured=true`
- `http_runtime_invoked=true`
- `network_invoked=true`
- `java_runtime_invoked=false`
- `candidate_generated=true`
- `runtime_status=http_runtime_success`
- `extraction_status=extracted`
- `schema_payload_status=ddl_derived_schema_json`
- `schema_table_count=1`
- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
- `no_upstream_source_or_jar_vendored=true`

The adapter metadata correctly reports that the adapter did not run DB,
checker, timing, local metrics, or verifier itself. DB/checker/timing were run
by the user facade after candidate generation, as recorded in the ledger.

No secret values were present in the committed audit summaries.
