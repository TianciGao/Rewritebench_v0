# POCR Step 5 Repair-1 PG40 Diagnostic Quality Review v0

This packet reviews the existing Direct LLM Repair-1 PostgreSQL PG40 checkpointed POCR annotation and replay artifacts. It reads the local annotation JSONL, manifest, checkpoint, and temp replay CSVs without calling any API, generating new annotations, rerunning replay, or computing official POCR.

Summary:
- Local annotation artifact present: true.
- Local replay artifact present: true.
- Schema-valid annotation rows reviewed: 35.
- Invalid/timeout rows: 5 (3 malformed JSON, 2 timeout).
- Transformation-supported operation atoms reviewed: 32.
- Possible over-accept findings: 0.
- Possible under-accept / strict-span rejection findings: 10.
- Exemplar classification: `accepted_with_boundary`.

This is diagnostic support only. This is not official POCR. No route-level POCR score is emitted. No paper-facing metric is promoted.
