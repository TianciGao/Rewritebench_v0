# Remaining Blockers

Identifier quoting is only partially closed.

Fixed by this task:

- Generated candidate SQL with quoted PostgreSQL DDL identifiers now executes for the five generated-candidate target rows.
- `CONS_0037` moved from candidate execution failure to exact/result-consistent.
- `CONS_0036`, `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` moved from candidate execution failure to candidate executable plus checker mismatch.

Still blocked:

- `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012` remain no-candidate rows because the external Calcite runtime rejects double-quoted source identifiers before candidate generation.
- `CONS_0036` has a label-only checker mismatch (`C` vs `c`) with value-exact result under strict labels.
- `LONGTAIL_0011`, `LONGTAIL_0012`, and `LONGTAIL_0013` have value mismatches after the quoting fix and require semantic review.
- DATETIME/TIMESTAMP handling remains separate.
- PORT source-role handling remains separate.
- Schema-fallback execution policy remains separate.

These blockers should not be bundled into this narrow identifier-folding fix.
