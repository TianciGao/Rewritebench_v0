# Direct LLM Provider Adapter Contract v0

Task: `direct_llm_provider_adapter_contract_v0`

Branch: `feature/case-package-v2-external-schema`

Scope:
- Create a D035 user-facing Direct LLM original adapter scaffold.
- Keep route-specific LLM code under `baselines/direct_llm_original/`.
- Use environment-variable provider configuration only.
- Add a Repair-1 future-route design note without implementing Repair-1.
- Run only focused unit tests and a fake-provider smoke over two PostgreSQL rows.

Result:
- `direct_llm_original` adapter scaffold was created.
- Provider contract supports OpenAI-compatible chat/completions endpoints, GPTSAPI aliases, fake-provider smoke, and fail-closed handling.
- Prompt and extraction contracts are explicit and conservative.
- No live API call was made.
- No full Track A run, metrics computation, verifier pass, paper output, retained-evidence promotion, or leaderboard output occurred.

Key files:
- `baselines/direct_llm_original/adapter.py`
- `baselines/direct_llm_original/README.md`
- `baselines/direct_llm_repair_1/README.md`
- `tests/user_entry/test_direct_llm_adapter.py`

Next safe action:
- Run a bounded canonical user-facade Direct LLM original smoke only when provider credentials are available and live calls are explicitly enabled.
