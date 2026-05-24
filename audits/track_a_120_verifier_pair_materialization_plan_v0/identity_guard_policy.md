# Identity Guard Policy

Identity guard is required for every future verifier row before any Semantic Equivalence Rate interpretation.

## Pair Types

- Source-vs-source identity guard: run the verifier on `source_sql_path` against itself with the same schema context.
- Candidate-vs-candidate identity guard: run the verifier on `candidate_sql_path` against itself with the same schema context.
- Source-vs-candidate actual verifier pair: run the verifier on `source_sql_path` against `candidate_sql_path` only after both identity guards are valid enough to trust the tool/model for that row.

## Recording Identity/Modeling Gaps

Identity/modeling gaps must be recorded separately from method behavior with verdicts such as `unknown`, `timeout`, `unsupported`, `not_implemented`, `tool_error`, `no_verifier_support`, or `not_attempted`. A row with an identity guard gap must not contribute to corrected `V_equiv` or `V_non`.

## SER Promotion Boundary

Identity guard failures block SER promotion because they show the verifier cannot prove even a self-comparison for the row under the selected schema/modeling setup. Treating source-vs-candidate output as semantic evidence after a failed identity guard would confound verifier limitations with rewrite correctness.

Identity guard failures are verifier-support limitations, not rewrite-method failures. Local checker exactness is only an eligibility gate and must never substitute for formal verifier equivalence.

## Corrected Decidable Denominator

Only rows with passing source-vs-source and candidate-vs-candidate identity guards, plus a decidable source-vs-candidate verdict, may enter the corrected decidable denominator:

`SER = corrected_equivalent / (corrected_equivalent + corrected_non_equivalent)`

No SER is computed by this packet.
