# Provider Client Boundary

The shared configuration plan covers provider transport settings, not route semantics.

Direct LLM generation and POCR annotation may use the same OpenAI-compatible transport layer. Prompt construction remains route-specific. POCR annotation schema is distinct from baseline candidate-generation prompts and output schemas.

Sharing configuration does not merge route evidence:

- Direct LLM original and Direct LLM Repair-1 remain separate routes.
- Adapted R-Bot and adapted LLM-R2 remain separate diagnostic routes.
- POCR Stage A annotation remains separate from candidate SQL generation.
- Candidate SQL, annotation JSONL, Stage B validation, timing, checker exactness, and paper metrics remain separate artifacts.

Provider call metadata may include provider label, model label, base URL host, call timestamp, token counts if available, status, and error type. It must not include API key values, bearer tokens, or raw `Authorization` headers.

One shared config does not mean shared prompt, shared output schema, shared denominator, shared evidence status, official POCR, or paper-facing metric promotion.
