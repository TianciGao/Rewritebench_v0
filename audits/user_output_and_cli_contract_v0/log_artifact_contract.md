# Log Artifact Contract

Log artifacts live under `output/logs/<run_id>/`.

Expected files:

- `command.log`: invoked command, resolved run ID, selected output roots, and high-level lifecycle events.
- `adapter_stdout.log`: adapter stdout capture when safe to expose.
- `adapter_stderr.log`: adapter stderr capture when safe to expose.
- `engine_env.json`: local engine/environment probe summary with secrets redacted.
- `failures.log`: human-readable failure/event log.
- `timing.log`: timing lifecycle log when timing is enabled.
- `verifier.log`: verifier lifecycle log when verifier support is enabled.

Logs must avoid credentials, API keys, private endpoints, and unnecessary absolute local paths. Raw stdout/stderr should be bounded and sanitized where possible.

Logs are local diagnostic artifacts only and are not retained evidence or official reports.
