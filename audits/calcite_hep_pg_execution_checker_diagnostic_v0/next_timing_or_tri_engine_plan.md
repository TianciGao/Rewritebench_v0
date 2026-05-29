# Next Timing Or Tri-Engine Plan

PostgreSQL-only timing is safe to authorize only for the 20 rows that were exact/result-consistent in this diagnostic pass. Timing should remain disabled for mismatch, execution-failed, and no-candidate rows.

Recommended next timing scope, if authorized separately:

- Engine: PostgreSQL only.
- Route: `calcite_hep_fail_closed`.
- Rows: the 20 exact rows from this audit.
- Exclusions: 7 no-candidate rows, 2 source-execution failures, 8 candidate-execution failures, and 3 checker mismatches.
- Continue to write only under a `/tmp` D035 output root unless a separate output-promotion policy is authorized.

Blocked before MySQL/Spark or full 120:

- Calcite identifier quoting causes PostgreSQL candidate execution failures on uppercase/mixed-case schemas.
- PORT rows with backtick source SQL are not suitable for PostgreSQL-only source execution.
- Schema-fallback candidates all failed and need manual review or runtime/schema handling improvements.
- MySQL and Spark Calcite route behavior has not been staged or validated.
- Official metrics and paper-facing outputs remain unauthorized.
