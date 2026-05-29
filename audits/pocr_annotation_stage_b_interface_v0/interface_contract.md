# Interface Contract

## Scope

This scaffold defines interfaces for POCR Stage A candidate annotation and Stage B evidence validation. It does not connect to `user_run.py`, `user_output.py`, `local_metrics.py`, `src/cli`, user-run output, top-level reports, or top-level results.

D036 remains the source-of-truth decision: operation atoms and semantic guard atoms come only from root-level case-local `skills.md` files at:

```text
cases/<POOL>/<CASE_ID>/skills.md
```

No atom is inferred from taxonomy tags, source SQL, positive SQL, negative SQL, candidate SQL, retained evidence, or performance behavior.

## Stage A Annotation Schema

The annotation schema version is `pocr_candidate_annotation_v1`.

Required row fields:

- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_id` or `candidate_path`
- `annotation_schema_version`
- `atoms`

Each atom judgment contains:

- `atom_id`
- `atom_type`: `operation_atom` or `semantic_guard_atom`
- `expected`: `true`
- `observed_status`: `implemented`, `not_implemented`, `contradicted`, `unclear`, or `not_applicable`
- `rationale_short`
- `evidence_refs`
- `confidence`: `high`, `medium`, or `low`

Stage A alone does not count atoms as the POCR numerator. It is a structured candidate annotation interface only.

## Prompt Builder

`build_annotation_prompt` accepts:

- parsed `SkillContract`
- source SQL text
- candidate SQL text
- optional positive SQL text
- optional negative SQL text
- engine
- method ID
- route ID
- candidate ID or candidate path

The prompt is deterministic and instructs any future model to judge only atoms from `skills.md`, not invent atoms, keep operation atoms separate from semantic guards, output strict JSON, mark uncertainty as `unclear`, and not use speedup or runtime as evidence.

## Annotation Client

`FakeAnnotationClient` supports offline fixture mode and returns a supplied structured annotation.

Future OpenAI-compatible live mode is represented by a fail-closed placeholder:

- no live API call is implemented in this task;
- no API key is read;
- live mode raises unless explicitly enabled, and then still raises because the live client is not implemented in this scaffold.

## Stage B Evidence Validation

`validate_stage_b` accepts:

- parsed `SkillContract`
- Stage A `CandidateAnnotation`
- optional candidate SQL text or path
- fixture-only synthetic evidence references

Stage B validates schema consistency, atom ID membership, duplicate atom IDs, missing atom judgments, invalid statuses, malformed evidence refs, and candidate path/text consistency. Without independent evidence, atoms remain `insufficient_evidence`.

Evidence statuses:

- `validated`
- `rejected`
- `insufficient_evidence`
- `schema_invalid`
- `atom_not_in_contract`

Rejected evidence sources include:

- LLM rationale alone
- speedup or timing
- taxonomy tags
- evidence refs for a different atom

## Row Draft

`POCRRowDraft` is a row-level diagnostic holder for future integration. It can store denominator eligibility placeholders, skill/annotation presence, Stage B status, validated operation atom count, expected operation atom count, and boundary text.

It does not aggregate route-level POCR and does not produce official paper metrics.
