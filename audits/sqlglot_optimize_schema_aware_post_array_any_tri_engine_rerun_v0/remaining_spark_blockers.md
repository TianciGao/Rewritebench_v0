# Remaining Spark Blockers

Two Spark rows remain non-exact after the MySQL guard rerun.

## CONS_0005 / Spark

Status:

- source executable: true
- candidate executable: true
- checker attempted: true
- exact/result-consistent: false
- failure bucket: `mismatch`

Prior triage classified this as a semantic mismatch candidate because source and candidate row counts differ. This remains separate from the MySQL `ARRAY_ANY` guard.

Recommended next action:

- keep as `spark_semantic_mismatch_candidate`;
- do not time this row;
- do not include it in exact-result local timing;
- triage SQLGlot Spark rewrite semantics separately before larger Spark optimize trials.

## CONS_0036 / Spark

Status:

- source executable: true
- candidate executable: true
- checker attempted: true
- exact/result-consistent: false
- failure bucket: `mismatch`

The checker artifact reports a label-only mismatch diagnostic with `value_exact=true`, `label_exact=false`, and `label_only_mismatch=true`.

Recommended next action:

- keep as `spark_label_only_mismatch_candidate`;
- do not silently normalize labels in this task;
- require a separate checker normalization policy authorization before treating it as exact.
