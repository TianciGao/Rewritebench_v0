# Stage B Evidence Source Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

The active user-facing Stage B path uses `src/sql_rewrite_bench/pocr/operation_evidence_policy.py`.

Evidence policy checks:

- `candidate_sql_span` alone is presence evidence only.
- `source_sql_span` alone is not operation support.
- `positive_sql_span` alone is not operation support.
- `source_candidate_diff:changed` must be paired with candidate-specific or positive-aligned span evidence for transformation support.
- Candidate-specific or positive-aligned spans without `source_candidate_diff:changed` are presence-only.
- If the candidate normalizes as source-like/no-op, cited spans prove presence only and do not become transformation support.
- `semantic_guard_atom` refs are validated as guard evidence but are not operation numerator.
- Unsupported evidence refs, LLM rationale, speedup, timing, taxonomy, file paths, and prose-only refs fail closed or are rejected by the evidence contract.

The PG40 pilot no-op row metrics reported zero transformation-supported operation atoms, which is consistent with no-op being a control route rather than a reference.

Verdict: `pass`.

Boundary retained: candidate/source/positive span presence alone is not operation support. Stage B transformation evidence is required before an atom enters the POCR numerator.
