# Secret Handling Policy

API key values must never be printed, written, staged, committed, or included in audit packets.

Logs and manifests may record the environment variable name used to find a key, for example `SQLRB_LLM_API_KEY` or `GPTSAPI_API_KEY`. They must not record the value.

If a `.env` file exists locally, it must not be committed.

Changed-file and staged secret scans remain required for any live-capable task, even when the task is documentation-only.

Safe metadata:

- provider label
- model label
- base URL domain or host when appropriate
- call timestamp
- token counts if available
- call status or error type
- API key environment variable name

Unsafe metadata:

- API key values
- bearer tokens
- raw `Authorization` headers
- copied provider secrets
- `.env` file contents

No API keys were read in this task.

API key values must never be printed.
