# Spark Zero Review

This is not official POCR.

No route-level official POCR score is emitted.

No paper-facing metric is promoted.

Direct LLM Repair-1 Spark remains at promotion-diagnostic POCR@planned=0.000000000000 and POCR@candidate=0.000000000000 after retry. Micro-average is diagnostic only and not the paper formula.

Row-level Spark evidence after retry:

- `PERF_0006`: annotation_status=`schema_invalid`, expected_operation_atoms=3, supported=0, presence_only=0, insufficient=0, fail_closed_status=`schema_invalid`
- `CONS_0005`: annotation_status=`schema_valid`, expected_operation_atoms=3, supported=0, presence_only=0, insufficient=3, fail_closed_status=`none`
- `PORT_0003`: annotation_status=`schema_valid`, expected_operation_atoms=3, supported=0, presence_only=2, insufficient=1, fail_closed_status=`none`
- `LONGTAIL_0011`: annotation_status=`schema_valid`, expected_operation_atoms=2, supported=0, presence_only=1, insufficient=1, fail_closed_status=`none`
- `LONGTAIL_0022`: annotation_status=`schema_invalid`, expected_operation_atoms=3, supported=0, presence_only=0, insufficient=0, fail_closed_status=`schema_invalid`

Interpretation: the zero is not only a total annotation outage. Three rows are schema-valid, but Stage B found no transformation-supported operation atoms; it recorded three presence-only operation atoms and five insufficient-transformation-evidence atoms across the route-engine slice. Two rows remain fail-closed after retry because the retry response was still malformed and replay represented them as schema-invalid fail-closed rows.

Recommended review: inspect the Spark source-to-candidate diffs for the schema-valid rows before expanding Spark Repair-1 beyond a pilot. The likely risks are Stage B under-accept or evidence-ref weakness rather than no-op over-accept. This remains diagnostic support only.
