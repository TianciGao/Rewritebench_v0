# Verifier Pair Recovery Plan

SER is a primary correctness metric, but it is formal-verifier-evidence-only.

Policy reminders:

- Local checker exactness is not SER evidence.
- The verifier phase should operate over exact/result-consistent source-vs-candidate pairs only.
- SQLSolver and VeriEQL must not be run in this inventory task.
- Unknown, timeout, unsupported, not_implemented, tool_error, no_verifier_support, and not_attempted verifier outcomes must be reported separately and excluded from the decidable SER denominator.

Existing evidence is sufficient to construct a verifier-pair inventory without rerunning adapters:

| route_id | exact rows | eligible pair estimate | blocker estimate |
| --- | ---: | ---: | ---: |
| direct_llm_original | 102 | 102 | 0 |
| sqlglot_noop | 97 | 97 | 0 |
| sqlglot_optimize_schema_aware | 66 | 66 | 0 |
| calcite_hep_fail_closed | 81 | 81 | 0 |

The pair inventory can use:

- per-engine source-run `selected_cases.csv` for source SQL and case path
- aggregate/source ledgers for exact status and engine
- candidate SQL paths from source-run ledgers
- case manifests for external schema profile references

Recommended first bounded verifier-pass target after inventory:

1. Generate verifier-pair manifests only, without invoking SQLSolver or VeriEQL.
2. Start with a small exact-row subset across two routes, for example `direct_llm_original` and `sqlglot_noop` on PostgreSQL `PERF_0006` and `CONS_0036`, if those rows are exact and have candidate/source/schema paths.
3. Run verifier tools only in a separately authorized bounded verifier task.
