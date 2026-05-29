# Unsupported Rows Policy

The Direct LLM original frontier contains five `unsupported_engine` Spark rows:

- `PORT_0008` / `spark` / `PORT`
- `PORT_0012` / `spark` / `PORT`
- `PORT_0022` / `spark` / `PORT`
- `PORT_0024` / `spark` / `PORT`
- `PORT_0025` / `spark` / `PORT`

Policy:

- Repair-1 must not attempt these rows unless the source-engine support policy changes in a separately authorized task.
- These rows remain selected/planned denominator rows for the 120 route.
- They must be reported as unsupported boundary rows, not hidden or dropped.
- They are not Repair-1 prompt failures.
- They are not provider failures.
- They are not local checker mismatches.
- They are not verifier failures.

The future local metrics denominator remains 120 even though these rows have no final generated candidate under current policy.
