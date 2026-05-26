# Discrepancy Findings

## SQLGlot no-op

Classification: `count_match_but_speedup_differs`; `runtime_source_differs`.

Counts, rates, exact rows, timed rows, and failure bucket counts match prior canonical evidence. The exact+timed row set is identical. GM differs because the new run remeasured source and candidate runtimes with two measured repetitions, while prior canonical timing used five measured repetitions. Formula direction and exact/timed eligibility do not explain the discrepancy.

## SQLGlot optimize schema-aware

Classification: `count_match_but_speedup_differs`; `runtime_source_differs`.

Counts, rates, exact rows, timed rows, and failure bucket counts match prior canonical evidence. The exact+timed row set is identical. GM differs because the new run remeasured source and candidate runtimes with two measured repetitions, while prior canonical timing used five measured repetitions. Formula direction and exact/timed eligibility do not explain the discrepancy.

## Calcite HEP fail-closed

Classification: `blocked_runtime_env`; `timing_row_set_differs`; `runtime_source_differs`.

Prior canonical Calcite evidence had a configured Calcite runtime and produced 99 candidates, 81 exact rows, 80 timed rows, and GM 0.9852158585899714. The new reproduction lacked `SQLRB_CALCITE_HEP_CMD`, `SQLRB_CALCITE_HEP_JAR`, and `SQLRB_CALCITE_HEP_ROOT`, generated no candidates, and therefore produced no exact+timed rows. The new Calcite output is a blocked-runtime smoke/local diagnostic artifact, not replacement evidence.

## Cross-route conclusion

Failure bucket vocabulary is compatible. Timing rows are traceable in the new outputs. SQLGlot reproductions can be accepted as local diagnostic reproduction evidence with boundary, but their GM values should not replace canonical values without separate promotion authorization. Calcite cannot be accepted as a metric replacement because the runtime was blocked.
