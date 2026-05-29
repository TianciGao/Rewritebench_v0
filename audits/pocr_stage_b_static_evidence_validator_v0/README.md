# POCR Stage B Static Evidence Validator v0

This packet records a bounded Stage B static evidence-validation scaffold and diagnostic dry-run. It uses only existing Common-core `skills.md`, existing no-op candidate SQL artifacts, and prior Stage A annotation audit artifacts.

## Scope

- Candidate root inspected: `runs/user/common_core_pg_noop_db_checker/candidate_sql`
- Annotation artifact inspected: `audits/pocr_live_api_annotation_smoke_v0/safe_annotation_outputs.jsonl`
- Candidate rows resolved: 40/40
- Annotation artifact statuses: {'missing': 36, 'present': 3, 'schema_invalid': 1}
- Diagnostic static Stage B rows emitted: 40
- Static validated operation atoms in dry-run: 0
- Static rejected operation atoms in dry-run: 3

## Boundary

The static validator confirms only explicit evidence references such as `candidate_sql_span:<literal substring>`. It does not infer operation atoms from SQL text, taxonomy, checker exactness, runtime behavior, or LLM rationale. It does not compute official Positive Operation Coverage Rate and does not aggregate route-level POCR.
