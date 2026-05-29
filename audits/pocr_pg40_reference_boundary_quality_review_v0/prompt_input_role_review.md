# Prompt Input Role Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

The Stage A prompt builder at `src/sql_rewrite_bench/pocr/prompt_builder.py` was reviewed.

Prompt role checks:

- It instructs the annotator to judge only atoms explicitly defined in the case-local `skills.md` Atom Protocol.
- It says not to invent, rename, merge, split, or infer atoms from taxonomy, SQL text, runtime, speedup, or retained evidence.
- It separates `operation_atom` and `semantic_guard_atom` as provided.
- It includes source SQL and candidate SQL in separate sections.
- It includes positive SQL as "Optional positive SQL context".
- It says positive-aligned static refs are comparison evidence for a declared `skills.md` atom, not a source of atoms.
- It says an operation atom must not be marked implemented merely because a candidate preserves a source-side SQL fragment.
- It requires evidence that the candidate implements the transformation relative to source.
- It asks for `source_candidate_diff:changed` when the candidate differs from source in the atom-relevant region.
- It warns that source-like/no-op candidates should be `not_implemented` or `unclear` for transformation atoms.
- It requires strict JSON only.

Verdict: `pass_with_boundary`.

Recommended wording improvement before wider expansion: rename the positive section from "Optional positive SQL context" to "Optional positive SQL reference evidence, not atom source" for extra clarity. This is not a blocker because the current prompt already says positive-aligned refs are comparison evidence only and not an atom source.

Required boundary: positive SQL is reference evidence, not an atom source. skills.md is the only operation-atom source.
