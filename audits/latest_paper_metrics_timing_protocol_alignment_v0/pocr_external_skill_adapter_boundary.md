# POCR External Skill Adapter Boundary

Positive Operation Coverage Rate is deferred.

## Current Boundary

This task does not:

- implement POCR;
- create `skill/` directories;
- infer operation atoms;
- parse operation atoms from taxonomy tags;
- parse operation atoms from SQL text;
- parse operation atoms from `positive.sql`;
- change case packages;
- modify repository specs.

## Future Input Expectations

Future POCR integration depends on a collaborator-provided external script and schema for source SQL to positive SQL operation atoms.

Expected future inputs may include:

- operation atom schema version;
- expected operation atoms `A_exp_i`;
- adapter/model covered atoms `A_hat_i`;
- Stage A validation output for atom extraction;
- Stage B validation output for coverage/mapping evidence;
- case-local mapping from positive reference SQL to operation atoms;
- explicit N.A. reason where operation atoms are unavailable.

## Possible Future Case-Local Files

The exact names are not approved. Candidate names from D032 include:

- `skill/operation_atoms.yaml`
- `skill/semantic_guard_atoms.yaml`
- `skill/skill_definition.md`
- `skill/positive_reference_mapping.yaml`

## Integration Guardrails

- The schema must be explicit and versioned.
- Operation atoms must be reviewable and reproducible.
- POCR denominator `C_r` must be selected and versioned.
- Stage B evidence required for atom coverage must be specified before computation.
- POCR outputs must remain separate from timing/performance outputs.
- POCR must not be computed from local diagnostic label/tag metadata alone.
