# Direct LLM Repair-1 Bounded Live End-to-End Smoke

This audit packet records a bounded live Repair-1 end-to-end smoke over three actionable Direct LLM original frontier rows.

Scope:

- `CONS_0005/postgres` mismatch feedback
- `PERF_0062/mysql` mismatch feedback
- `LONGTAIL_0012/spark` candidate-execution-failed feedback

Counts:

- selected rows: 3
- unsupported-engine rows attempted: 0
- live calls: 3
- repaired candidates generated: 3
- candidate executable rows: 3
- exact rows: 3
- timed rows: 3
- fail-closed rows: 0

Provider/access status was healthy before the row run: env presence checks passed and `/v1/models` returned HTTP 200. Adapter metadata recorded `provider=openai_compatible`, `base_url_host=api.gptsapi.net`, `model_id=gpt-5.4`, and `live_call=true` for each selected row.

This is local diagnostic smoke evidence only. It is not Track A 120, not aggregate local metrics, not official SER, not paper-facing, and not retained evidence.
