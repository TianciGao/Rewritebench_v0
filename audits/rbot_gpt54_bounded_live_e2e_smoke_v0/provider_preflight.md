# Provider Preflight

Preflight was checked without printing or recording secret values.

- live gate: `SQLRB_LLM_ALLOW_LIVE=1`
- provider: `openai_compatible`
- base URL: configured; safe host observed as `api.gptsapi.net`
- model: `gpt-5.4`
- API key: present, value not printed or copied
- raw response saving: disabled for this smoke
- separate provider health check: not performed, to avoid an extra live request outside the selected benchmark rows

The only live provider calls in this task were the six selected PostgreSQL user-facade rows recorded in this audit packet.

No API key, token, or secret value was printed, written to the audit packet, staged, or committed.
