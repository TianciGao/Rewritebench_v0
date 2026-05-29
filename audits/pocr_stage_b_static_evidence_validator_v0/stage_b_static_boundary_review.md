# Stage B Static Boundary Review

The dry-run emitted 40 row-level diagnostic drafts. Stage status counts: {'annotation_missing': 36, 'insufficient_evidence': 2, 'schema_invalid': 1, 'static_evidence_rejected': 1}.

Stage B remains conservative:

- Stage A annotation alone is not evidence.
- LLM rationale is not independent evidence.
- Speedup, runtime, checker exactness, and taxonomy tags are not operation evidence in this task.
- Candidate SQL text alone does not validate an atom unless a Stage A annotation cites an explicit supported static evidence ref and the validator confirms that ref.
- `semantic_guard_atom` rows are not counted as operation coverage numerator.
- `official_pocr_computed` is false for every diagnostic row.
- No route-level POCR aggregation is produced.

The prior live-smoke artifact was route-compatible for the no-op diagnostic candidate root where schema-valid. The malformed `PERF_0006` provider row remains fail-closed as schema invalid.
