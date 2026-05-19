# Future Prompt: case_package_v2_batch_conversion_pilot_v0

Work only in `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

This is a writable branch-only conversion pilot. Do not modify `main`.

Use the read-only plan in:

- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_case_readiness.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_file_disposition_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_manifest_conversion_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_schema_externalization_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_evidence_runs_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_validation_consolidation_plan.csv`
- `audits/case_package_v2_batch_converter_plan_v0/v2_batch_converter_stop_conditions.csv`

Scope:

- Convert only cases whose manual-review blockers have been explicitly resolved.
- If no case is classified safe for writable conversion after review, stop and write a blocked audit packet.
- Treat `PERF_0006` as the canonical already-normalized example.
- Do not convert additional cases beyond `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.

Allowed writable actions after blockers are resolved:

- create direct `sql/pos_01.sql` and `sql/neg_01.sql` copies
- normalize manifest shape
- add schema_ref
- add evidence_ref
- add thin validation wrappers
- copy-first externalize schema assets
- copy-first externalize public-safe evidence
- retain compatibility directories and scripts

Forbidden:

- modifying main
- deleting case-local schema
- deleting evidence
- deleting runs
- changing case_sets
- changing inventory
- changing denominators
- changing paper results
- updating reports/results
- running DB/checker execution
- computing official metrics
- rendering paper tables
- creating leaderboard output

Validation:

- branch check
- YAML parse
- v2 reference validator
- protected path checks
- no case-local runs output
- no reports/results output
- no denominator or paper-result changes
- `git diff --check`

Commit only with explicit `git add`.
