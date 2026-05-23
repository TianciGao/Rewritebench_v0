# Next PostgreSQL Rerun Plan

The narrow fix is safe to rerun through the PostgreSQL Calcite diagnostic chain:

1. Rerun bounded PostgreSQL candidate generation for `calcite_hep_fail_closed`.
2. Review generated candidates and preserve no-candidate rows.
3. Rerun PostgreSQL execution/checker over generated candidates only.
4. If exact rows change, rerun exact-only PostgreSQL timing.
5. Reproject the local diagnostic route card with the full non-exact frontier visible.

Expected effects:

- Candidate execution coverage should improve for the generated identifier-quoting rows.
- Exact row count may increase by at least `CONS_0037`.
- Mismatch frontier may grow because rows previously blocked at candidate execution now reach the checker.

Do not treat this targeted validation as a replacement for the full PostgreSQL diagnostic chain rerun. Do not run MySQL/Spark/full-120 until DATETIME/TIMESTAMP, PORT source-role, schema-fallback, and mismatch blockers are separately handled or accepted as denominator-visible limitations.
