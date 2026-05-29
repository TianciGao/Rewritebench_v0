# Direct LLM GPTSAPI 403 Access Probe v0

Goal: diagnose the GPTSAPI/OpenAI-compatible `HTTP 403` / `code 1010` seen during the Direct LLM original live smoke.

Conclusion:

- The provider/account/key path is usable when the request includes `User-Agent: SQL-RewriteBench/0.1`.
- `POST /v1/chat/completions` succeeded for both supported auth styles with that User-Agent.
- `GET /v1/models` succeeded with that User-Agent and listed `gpt-5.4`.
- The adapter-like request shape without a custom User-Agent reproduced `HTTP 403: error code 1010`.
- The one permitted facade adapter row also reproduced `HTTP 403: error code 1010` before the fix.
- Adapter fix applied: `baselines/direct_llm_original/adapter.py` now sends `User-Agent: SQL-RewriteBench/0.1`.
- Unit coverage added in `tests/user_entry/test_direct_llm_adapter.py`.

Validation:

```text
python -m pytest tests/user_entry/test_direct_llm_adapter.py
9 passed
```

No post-fix live benchmark row was run because the task allowed at most one final adapter smoke, and that one-row smoke was used to confirm the pre-fix adapter failure mode.

