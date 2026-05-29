# Reference Boundary Summary

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.

Correct reference roles for POCR:

- `source.sql` is the transformation origin and source-side semantic oracle input.
- Positive SQL is the trusted positive rewrite / target-direction reference evidence. positive SQL is reference evidence, not an atom source.
- `skills.md` is the only operation-atom source. It is also the only source for `semantic_guard_atom` contracts.
- Candidate SQL is the method output under evaluation.
- SQLGlot no-op is a candidate/control route, not a reference.

Boundary rules:

- SQLGlot no-op must not be used as a positive reference.
- Positive SQL must not be used as the operation atom source.
- Candidate SQL must not invent atoms.
- Taxonomy labels must not invent atoms.
- candidate/source/positive span presence alone is not operation support.

Review verdict: `pass_with_boundary`. The current implementation separates these roles, and the remaining boundary is reporting discipline: PG40 diagnostic values must not be described as official POCR or Track A 120 evidence.
