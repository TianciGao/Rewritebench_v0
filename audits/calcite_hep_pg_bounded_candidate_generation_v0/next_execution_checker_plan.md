# Next Execution Checker Plan

Safe next action: authorize a separate PostgreSQL-only execution/checker diagnostic pass for the generated Calcite HEP candidates.

Recommended boundaries for that future task:

- Use only the PostgreSQL rows from this candidate-generation ledger.
- Execute only rows with `candidate_generated=true`; preserve the seven fail-closed rows as no-candidate rows.
- Keep timing disabled unless separately authorized.
- Do not run SQLSolver/VeriEQL in the execution/checker task.
- Do not compute official metrics or update paper reports/results.
- Record source execution, candidate execution, checker exactness, mismatch artifacts, and failure buckets under a `/tmp` D035 output root.
- Treat parse-only schema-fallback rows as manual-review candidates before promotion.

Blocked before tri-engine or full 120:

- MySQL/Spark Calcite rendering is not validated.
- Execution/checker closure for PostgreSQL candidates is not established.
- Timing/speedup is not authorized.
- Official metrics and paper-facing outputs remain unauthorized.
