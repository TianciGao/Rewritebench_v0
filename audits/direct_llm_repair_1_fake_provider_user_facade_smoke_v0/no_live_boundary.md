# No Live Boundary

No live provider call occurred.

The facade smoke was executed with:

- `SQLRB_LLM_PROVIDER=fake`
- `SQLRB_LLM_ALLOW_LIVE` unset for the command environment
- `SQLRB_LLM_API_KEY` unset for the command environment
- `GPTSAPI_API_KEY` unset for the command environment

Observed adapter metadata for both rows:

- `provider=fake`
- `live_call=false`
- `api_key_present=false`

No API key was required and no secret value was written.
