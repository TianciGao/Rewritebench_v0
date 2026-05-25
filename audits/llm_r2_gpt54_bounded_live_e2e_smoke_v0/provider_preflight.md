# Provider Preflight

- Live gate enabled: yes (`SQLRB_LLM_ALLOW_LIVE=1` was present).
- Provider policy: `openai_compatible`.
- Base URL env present: yes; value not printed or written.
- API key env present: yes; value not printed or written.
- Model: `gpt-5.4`.
- Separate provider health check: not run; the bounded user-facade smoke made exactly the selected-row live calls.
- Secret handling: no API key values were printed, written, staged, or committed.
