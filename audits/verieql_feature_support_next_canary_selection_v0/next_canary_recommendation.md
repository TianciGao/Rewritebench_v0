# Next Canary Recommendation

Recommendation: authorize exactly one future bounded VeriEQL canary for `PERF_0062 source_vs_positive pos_01`.

Primary pair:

- Case: `PERF_0062`
- Pool: `PERF`
- Pair type: `source_vs_positive`
- Source SQL: `cases/PERF/PERF_0062/sql/source.sql`
- Positive SQL: `cases/PERF/PERF_0062/sql/pos_01.sql`
- Schema context: `schemas/tpcds_perf0062_v0/postgres/ddl.sql`

Why this is the safest next pair found:

- One `SELECT` on source and one `SELECT` on positive.
- No `EXISTS` or `NOT EXISTS`.
- No nested `SELECT`.
- No window `OVER`.
- No date/time/interval expression.
- No outer join.
- No set operation.
- Positive rewrite is mainly comma-join to explicit inner-join normalization.
- Aggregates are basic `AVG` and `SUM`.

Known risks:

- VeriEQL aggregate support exists in tests/source structure, but some aggregate expression forms still have unsupported paths.
- The source uses literal `IN (...)` lists. This is not the confirmed unsupported `IN (SELECT ...)` shape, but `IN` predicates can still have edge cases.
- `PERF_0062` is not a CONS case. This is acceptable for feature-support canary discovery, but it should not be described as a CONS verifier canary.

Fallback pair:

- Case: `PORT_0024`
- Pair: `source_vs_positive pos_01`
- Reason: compact single-select aggregate/CASE shape without `EXISTS`, nested `SELECT`, date/interval, window, outer join, or set operation.
- Risk: PORT case role semantics and CASE expression support should be kept explicit; do not mix this with cross-engine correctness claims.

CONS-only fallback:

- Case: `CONS_0036`
- Pair: `source_vs_positive pos_01`
- Reason: avoids `EXISTS`.
- Risk: positive SQL contains a nested `SELECT`, which is a known source-level unsupported/high-risk feature. Use only if the team requires the next canary to be from CONS despite higher feature risk.

Recommendation for real run:

- Yes, a real run is recommended next, but only under a separately authorized task.
- Scope should be exactly one pair: `PERF_0062 source_vs_positive pos_01`.
- Use the existing staged VeriEQL root and external venv.
- Preserve local-only output under temporary or ignored output roots.
- Do not compute official Semantic Equivalence Rate.
- Do not update top-level reports/results or retained evidence.
