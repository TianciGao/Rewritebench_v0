# Canonicalization Policy Design

This is a design document only. It does not implement wrapper changes and does not authorize verifier coverage expansion.

## SQL Line-Shaping Policy

- Preserve SQLSolver's one-statement-per-line contract.
- Normalize each verifier input to exactly one SQL statement per physical line only after comment handling and statement-boundary checks.
- Strip or safely preserve leading line comments before one-line shaping.
- Avoid collapsing comment-prefixed SQL into invalid SQLSolver input. A leading `--` comment joined with SQL on the same line can comment out the SQL statement.
- Preserve an audit sidecar showing original source/candidate hashes, canonicalized-input hashes, and canonicalization family applied.
- Reject multi-statement input rather than guessing which statement should be verified.

## SQL Comment Policy

- Remove line comments that are metadata/provenance and not part of executable SQL before SQLSolver input generation.
- Remove block comments from SQLSolver input unless an explicit fixture proves Calcite/SQLSolver handles them safely in the target mode.
- Never modify committed source or candidate SQL. Canonicalized inputs must be temporary verifier inputs with metadata.
- Keep redacted excerpts of canonicalization decisions, not full hidden runtime dumps, in audit packets.

## Date / Interval Normalization Policy

- Treat PostgreSQL `DATE 'YYYY-MM-DD'` literals as a canonicalization target. Candidate forms such as `CAST('YYYY-MM-DD' AS DATE)` may be more stable for Calcite/SQLSolver; this requires fixture proof.
- Do not assume `DATE` literal and `CAST(... AS DATE)` normalization is semantics-preserving across all dialects; restrict to PostgreSQL same-engine verifier support with explicit canaries.
- Treat `INTERVAL` arithmetic as a separate gate. PostgreSQL forms such as `date '1995-01-01' + interval '1' year` and `INTERVAL '1 YEAR'` need Calcite-compatible shaping or exclusion.
- If interval canaries fail, interval rows remain outside first SQLSolver SER support scope.

## Schema DDL Canonicalization Policy

- Strip inline comments from DDL before SQLSolver input generation.
- Remove draft DDL preambles such as `DROP TABLE IF EXISTS` unless a canary proves SQLSolver accepts them safely.
- Normalize unsupported or PostgreSQL-specific types only through a documented mapping table.
- Proposed candidate mappings for canary testing: `DOUBLE PRECISION` to a Calcite-compatible floating type, `TIMESTAMP` to a supported timestamp/date representation if accepted, `TEXT` to `VARCHAR`, and `NUMERIC(p,s)` to the closest accepted decimal form.
- Do not canonicalize away constraints or column nullability unless the verifier support contract records that the abstraction is intentional and local-only.

## Identifier and Ordering Policy

- Quoted identifiers require a policy before PORT rows enter broader SQLSolver scope. Options are preserve quotes if Calcite accepts them, or map quoted identifiers to safe unquoted identifiers with a reversible table.
- `NULLS FIRST` / `NULLS LAST` must be treated as ordering semantics, not formatting. If SQLSolver cannot model them directly, these rows remain blocked or require a proved-safe rewrite for verifier input only.
- `ORDER BY` / `LIMIT` rows need dedicated canaries because order-sensitive semantics may interact with SQLSolver support limits.

## Feature Support Policy

- Add a DENSE_RANK / CTE ranking canary before including LONGTAIL ranking rows in broader verifier scope.
- Add window-function canaries by family, not as one broad bucket: `ROW_NUMBER`, `DENSE_RANK`, partitioned ranking, and aggregate-over-window should be separated.
- EXISTS, subquery, and function families should not be generalized from one passing CONS row. They need canaries before broad SER-support inclusion.
- Any family whose identity guard returns `UNKNOWN`, `TIMEOUT`, `unsupported`, or `tool_error` remains outside decidable SER support until fixed or explicitly scoped out.
