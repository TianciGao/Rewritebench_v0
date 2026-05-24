# Unsupported Boundary

Unsupported-engine rows were not selected for this smoke.

The excluded Direct LLM original frontier rows remain:

- `PORT_0008 / spark`
- `PORT_0012 / spark`
- `PORT_0022 / spark`
- `PORT_0024 / spark`
- `PORT_0025 / spark`

Repair-1 should not attempt these rows until a separate source-engine support
policy changes. The adapter scaffold already has fixture coverage that
`unsupported_engine_boundary_feedback` fails closed before provider invocation.

This smoke used only the two actionable feedback families:

- `checker_mismatch_feedback`
- `candidate_execution_error_feedback`
