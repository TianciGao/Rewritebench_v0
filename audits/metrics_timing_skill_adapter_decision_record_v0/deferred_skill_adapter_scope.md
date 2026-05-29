# Deferred Skill Adapter Scope

Positive Operation Coverage Rate is not implemented by this task.

## Deferral Rationale

POCR depends on curated operation atoms and a two-stage validation flow. A collaborator is preparing an external script for source SQL to positive SQL operation atoms. Implementing repository-side operation atom extraction before that script and schema stabilize would risk schema drift and unverifiable atom definitions.

## Explicitly Deferred

- POCR computation.
- `skill/` folder creation.
- Operation atom inference.
- Operation atom extraction from taxonomy tags.
- Operation atom extraction from SQL text.
- Operation atom extraction from `positive.sql`.
- Case package layout changes for skill assets.

## Future Case-Local Skill Surface

Future integration should be explicit and case-local after external-script review. Candidate file names may include:

- `skill/operation_atoms.yaml`
- `skill/semantic_guard_atoms.yaml`
- `skill/skill_definition.md`
- `skill/positive_reference_mapping.yaml`

Exact names and schema remain pending.

## Required Future Gate

Before any `skill/` folder is created or populated, the project needs a separately authorized integration contract covering schema, validation, ownership, and public-reporting boundary.
