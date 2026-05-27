# Response Schema Review

Expected Stage A response shape is a single JSON object matching `pocr_candidate_annotation_v1` with `case_id`, `pool`, `engine`, `method_id`, `route_id`, a candidate reference, and one atom judgment for every atom in case-local `skills.md`.

Required atom fields are `atom_id`, `atom_type`, `expected`, `observed_status`, `rationale_short`, `evidence_refs`, and `confidence`. The validator also checks case/pool/engine/method/route binding, atom membership, duplicate and missing atom judgments, observed status, confidence, and non-empty rationale.

Observed failure classes are dominated by provider-call failures during retry, not schema validator strictness. The 150 retry calls all produced `provider_call_failed` with `RuntimeError`; safe error excerpts identify HTTP 401 / insufficient balance. Earlier Track A failures include malformed JSON and one timeout, but the retry batch did not reach usable model output.

The validator is correctly fail-closed for missing/invalid output. No evidence suggests that relaxing schema validation would fix the retry failure class.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
