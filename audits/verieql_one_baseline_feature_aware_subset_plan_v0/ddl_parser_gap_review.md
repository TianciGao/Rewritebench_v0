# DDL Parser Gap Review

Current gap:
- The wrapper's current CREATE TABLE parser can truncate parameterized types when a column type contains parentheses.
- Example observed in the tiny exact-candidate pass: `VARCHAR(32)` appeared in VeriEQL metadata as `VARCHAR(32`.

Impact:
- 17 of 35 exact rows have parameterized DDL types that trigger this current-parser rough edge.
- A truncated type did not block `CONS_0036`, but it should not be accepted as stable before broader exact-candidate verifier use.

Affected exact rows with current parser malformed type metadata:
- `PERF_0006`
- `PERF_0007`
- `PERF_0008`
- `PERF_0013`
- `PERF_0017`
- `PERF_0019`
- `PERF_0024`
- `PERF_0033`
- `PERF_0034`
- `PERF_0035`
- `CONS_0007`
- `CONS_0010`
- `CONS_0011`
- `CONS_0012`
- `CONS_0024`
- `CONS_0036`
- `CONS_0037`

Required hardening before expansion:
- Parse CREATE TABLE column lists with balanced parentheses instead of stopping at the first closing parenthesis.
- Preserve complete type strings such as `VARCHAR(32)`, `NUMERIC(15,2)`, and `DECIMAL(9,2)`.
- Keep canonicalized table/column identifiers while preserving traceability to the original DDL path.
- Add focused regression tests for DDL with parameterized types.

