# Support Readiness File Review

## Files Reviewed

Primary files under `/home/tianci_gao/code/sql-rewrite-bench/reports/baseline_smoke/`:

- `sqlsolver_verieql_support_readiness_v0.json`
- `sqlsolver_verieql_support_readiness_execute_refused_v0.json`

## `sqlsolver_verieql_support_readiness_v0.json`

This is a static support-readiness report, not verifier execution output.

Key fields:

- `command`: `baseline-smoke-sqlsolver-verieql-readiness`
- `candidate_set`: `pg-native-9`
- `case_count`: `9`
- `claim_boundary`: `sqlsolver_verieql_support_readiness_only_not_equivalence_or_execution`
- `equivalence_execution_attempted_count`: `0`
- `support_analysis_attempted_count`: `0`
- `ok`: `true`

Guardrails disabled:

- SQLSolver execution
- VeriEQL execution
- SMT solver execution
- database execution
- SQLGlot generation
- Calcite execution
- LLM execution
- dependency installation
- artifact download
- case artifact writes

## Case Classification

| case_id | pool | status | SQLSolver risk | VeriEQL risk | usefulness | reason |
|---|---|---|---|---|---|---|
| `PERF_0006` | performance | maybe | medium | medium | medium | Clean analytical SQL shape, but aggregate and bag-semantics support uncertain. |
| `PERF_0008` | performance | maybe | medium | medium | medium | Clean analytical SQL shape, but aggregate and bag-semantics support uncertain. |
| `PERF_0013` | performance | exclude | high | high | medium | Interval/date semantics raise symbolic encoding risk. |
| `PERF_0017` | performance | exclude | high | high | medium | Interval/date semantics raise symbolic encoding risk. |
| `PERF_0024` | performance | maybe | high | high | high | Correlated nested subqueries are semantically useful but likely difficult. |
| `PERF_0033` | performance | maybe | medium | medium | medium | Clean analytical SQL shape, but aggregate and bag-semantics support uncertain. |
| `PERF_0054` | performance | maybe | medium | medium | medium | Clean analytical SQL shape, but aggregate and bag-semantics support uncertain. |
| `CONS_0007` | consistency | support_candidate | medium | medium | high | Compact Calcite-derived consistency case; best bounded first support candidate. |
| `CONS_0012` | consistency | maybe | high | high | high | Useful semantic case, but LIMIT/OFFSET and correlation raise subset risk. |

## `sqlsolver_verieql_support_readiness_execute_refused_v0.json`

This file records the intentional refusal to execute tools through the readiness scaffold.

Important fields:

- `ok`: `false`
- `type`: `execution_not_supported`
- `message`: `This scaffold does not execute SQLSolver or VeriEQL. It only emits a static support-readiness report.`
- `claim_boundary`: `sqlsolver_verieql_support_readiness_only_not_equivalence_or_execution`

## Interpretation

The baseline smoke folder supplies static support-readiness evidence only. It does not prove tool availability, does not prove equivalence, and does not provide new-repo Semantic Equivalence Rate input.
