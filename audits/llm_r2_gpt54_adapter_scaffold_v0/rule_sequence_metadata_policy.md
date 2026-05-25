# Rule Sequence Metadata Policy

LLM-R2 can produce or depend on rule-sequence concepts in the official system.
In this scaffold, rule sequence is metadata only.

Policy:

- A rule-only response is not candidate SQL.
- Rule sequence must not be treated as emitted SQL.
- Rule sequence must not be scored as an optimizer trace.
- No rule-system execution is authorized in fake mode.
- No checkpoint or demonstration selector is used in fake mode.

Future rule-system integration requires a separate runtime contract, including
input shape, output shape, failure buckets, provenance, and D035 user-facade
handoff.
