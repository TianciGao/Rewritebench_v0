# Representative Failure Samples

Safe redacted excerpts only. No API keys, raw auth headers, or raw provider payloads are included.

- `direct_llm_original` / `mysql` / `PERF_0006`: `output_json_contract_or_truncated_json` -> `Expecting ',' delimiter: line 1 column 712 (char 711)`
- `direct_llm_original` / `mysql` / `PERF_0035`: `unknown_provider_or_schema_failure` -> `provider request failed: HTTP 520: error code: 520`
- `direct_llm_original` / `postgres` / `CONS_0012`: `network_or_provider_timeout` -> `The read operation timed out`
- `direct_llm_repair_1` / `mysql` / `CONS_0011`: `provider_config_issue_insufficient_balance_or_unauthorized` -> `provider request failed: HTTP 401: {"error":"Balance is insufficient"}`
- `sqlglot_optimize_schema_aware` / `mysql` / `PERF_0008`: `no_candidate_non_retryable` -> `checkpointed diagnostic row; no official POCR`
- `direct_llm_original` / `mysql` / `PERF_0007`: `output_json_contract_or_truncated_json` -> `Expecting ',' delimiter: line 1 column 715 (char 714)`
- `direct_llm_original` / `mysql` / `PERF_0008`: `output_json_contract_or_truncated_json` -> `Expecting ',' delimiter: line 1 column 689 (char 688)`
- `direct_llm_original` / `mysql` / `PERF_0024`: `output_json_contract_or_truncated_json` -> `Expecting ',' delimiter: line 1 column 638 (char 637)`

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
