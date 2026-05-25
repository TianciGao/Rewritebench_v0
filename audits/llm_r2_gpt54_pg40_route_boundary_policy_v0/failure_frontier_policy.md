# Failure Frontier Policy

The PG40 failure frontier from `audits/llm_r2_gpt54_pg40_bounded_local_diagnostic_v0/` is:

- exact: 39
- mismatch: 0
- candidate_execution_failed: 1
- candidate_execution_failed row: `LONGTAIL_0011`
- fail-closed rows: 0
- source-like/no-op diagnostic row: `CONS_0037`

`LONGTAIL_0011` remains a candidate-execution boundary and must stay visible in the PG40 denominator. It was not replaced, dropped, or converted into a checker/verifier finding.

These failures are adapted-route behavior diagnostics. They are not hard-negative checker controls and not verifier failures. Local checker exactness is not official SER evidence, and the absence of a verifier run means no official semantic-equivalence claim is made.

`CONS_0037` is a source-like/no-op diagnostic row only. It is not a POCR row, not a ranking metric, and not a reason to remove the row from the selected denominator.
