# Adapter Implication

One permitted facade adapter row was run before applying the fix:

```text
run_id=direct_llm_gptsapi_403_access_probe_v0_adapter_one_row
case_id=PERF_0006
engine=postgres
candidate_generated_rows=0
adapter_call_status=request_failed
adapter_failure_bucket=request_failed
adapter_failure_summary=HTTP 403: error code 1010
```

The direct provider probe succeeded with `User-Agent: SQL-RewriteBench/0.1`, while the adapter-like request without a custom User-Agent failed with the same `403 / 1010`.

Classification: adapter request-header mismatch.

Fix applied:

- `baselines/direct_llm_original/adapter.py` now adds `User-Agent: SQL-RewriteBench/0.1` to OpenAI-compatible requests.
- `tests/user_entry/test_direct_llm_adapter.py` now asserts that `_call_openai_compatible` sends this header.

Validation:

```text
python -m pytest tests/user_entry/test_direct_llm_adapter.py
9 passed
```

No second live adapter row was run after the fix because the task limited benchmark rows to at most one final adapter smoke.

