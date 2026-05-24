# Implementation Plan

This plan is for a later, separately authorized implementation task. No code is changed in this design packet.

## Sequence

1. Add wrapper canonicalization functions behind an explicit SQLSolver-only verifier input layer.
2. Add unit tests for each canonicalization family: SQL line shaping, comment stripping, date/interval normalization, DDL canonicalization, identifier mapping, and null-order preservation.
3. Add fixture tests that prove original SQL files remain unchanged and canonicalized verifier inputs are temporary/local-only.
4. Run non-benchmark identity canaries only after implementation is reviewed.
5. Rerun the same 8 bounded SQLGlot no-op PostgreSQL pairs, with identical pair selection and identity guards.
6. Only if the same 8-pair run has stable identity guards and clear non-decidable reporting, authorize the SQLGlot no-op PostgreSQL 35 exact subset.
7. Only after SQLGlot no-op PostgreSQL 35 is stable, consider broader route/engine coverage from the 346-pair manifest.

## Implementation Constraints

- Do not modify benchmark source SQL, candidate SQL, cases, schemas, or ledgers.
- Canonicalized inputs must be generated under local verifier runtime output only.
- Every canonicalization step must be recorded in metadata with original and canonicalized hashes.
- Unknown, timeout, unsupported, not-implemented, tool-error, no-verifier-support, and not-attempted outcomes remain outside the decidable SER denominator.
- The implementation must not promote local checker exactness as SER evidence.

## Initial Test Targets

- Unit tests for `_read_sql_line` replacement behavior or a new canonicalizer, without invoking SQLSolver.
- Unit tests for schema DDL canonicalization with inline comments, `DROP TABLE`, `DOUBLE PRECISION`, `TEXT`, `TIMESTAMP`, and `NUMERIC(p,s)`.
- Dry-run artifact tests confirming command construction and redacted metadata.
- Later canary execution only after a separate task authorizes SQLSolver runtime.
