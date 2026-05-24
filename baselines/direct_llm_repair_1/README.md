# Direct LLM Repair-1 Future Route

This directory is a design placeholder for a future route:

- `route_id = direct_llm_repair_1`
- `method_id = direct_llm_repair_1`

Repair-1 is not implemented in this task.

Required future contract:

- consume the Direct LLM original candidate and status metadata
- consume execution/checker feedback from the user-run pipeline
- record the repair prompt template id
- record feedback type and source
- record original candidate id and repaired candidate id
- write repaired candidate SQL only when extraction succeeds unambiguously
- preserve the original candidate and failure trace
- remain a separate route from `direct_llm_original`
- use environment-variable provider configuration only
- keep local-only, non-official, non-paper, non-leaderboard boundary flags

Repair-1 must not silently mutate Direct LLM original outputs. It requires a
separate authorization and audit packet before implementation.
