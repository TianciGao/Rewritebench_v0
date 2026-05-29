# Repair-1 Future Contract

Repair-1 was not implemented in this task.

Future route:
- `route_id = direct_llm_repair_1`
- `method_id = direct_llm_repair_1`

Required future inputs:
- Direct LLM original candidate SQL.
- Direct LLM original status metadata.
- Source SQL.
- Schema/DDL context.
- Execution failure, checker mismatch, or preflight feedback from the user-run pipeline.

Required future metadata:
- repair prompt template id.
- feedback type and source.
- original candidate id.
- repaired candidate id.
- provider/model/generation settings.
- extraction policy id.
- local-only and non-official boundary flags.

Policy:
- Repair-1 must be a separate route.
- Repair-1 must not silently mutate `direct_llm_original` output.
- Repair-1 must preserve original candidate traceability.
- Repair-1 needs a separate authorization, implementation task, tests, and audit packet.
