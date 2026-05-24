# Unsupported Boundary

Repair-1 currently attempts only actionable Direct LLM original frontier rows:

- `mismatch=10`
- `candidate_execution_failed=3`

The five unsupported Spark rows from the Direct LLM original frontier remain
excluded:

- `PORT_0008 / spark`
- `PORT_0012 / spark`
- `PORT_0022 / spark`
- `PORT_0024 / spark`
- `PORT_0025 / spark`

Rows carrying `unsupported_engine_boundary_feedback` or `unsupported_engine`
are failed closed before any provider call. This is a source-engine/support
boundary, not a Repair-1 candidate failure.

No case membership, denominator, paper result, retained evidence, or official
metric changed.
