# Non-Timed Frontier

The exact gate left 54 selected rows outside timing. These rows remain denominator-visible and were not silently dropped.

| Non-timing reason | Rows |
| --- | ---: |
| candidate_execution_failed | 9 |
| label_only_mismatch | 16 |
| mysql_unsupported_array_any | 1 |
| semantic_mismatch | 9 |
| sqlglot_optimize_failed | 5 |
| sqlglot_parse_failed | 5 |
| sqlglot_schema_parse_failed | 4 |
| unsupported_engine | 5 |

Policy notes:

- `CONS_0005/mysql` remains fail-closed with `mysql_unsupported_array_any`.
- `CONS_0005/spark` remains a semantic mismatch and was not timed.
- `CONS_0036/spark` remains a label-only mismatch under current strict-label policy and was not timed.

Future work should handle frontier triage separately from timing. Timing should remain exact-gated unless a later authorized checker or route-policy change moves rows into the exact set.
