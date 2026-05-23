# Exact Gate Review

Eligibility criteria used for verifier execution:
- `candidate_generated=true`
- `candidate_preflight_passed=true`
- `source_execution_status=source_execution_success`
- `candidate_execution_status=candidate_execution_success`
- `checker_status=checker_success`
- `exact_status=exact`

Gate results:

| case_id | candidate generated | preflight passed | source executable | candidate executable | checker success | exact | verifier eligible |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONS_0036 | yes | yes | yes | yes | yes | yes | yes |
| PERF_0077 | yes | yes | yes | yes | yes | yes | yes |
| PERF_0082 | yes | yes | yes | yes | yes | yes | yes |

Counts:
- Selected candidate rows: 3.
- Exact candidate rows: 3.
- Verifier attempted rows: 3.
- Ineligible selected rows: 0.

Local result checker exactness was not used as verifier equivalence evidence. It was used only to gate source-vs-candidate pairs into the local VeriEQL pass.

