# Pool Summaries

| pool | planned/selected | generated | fail-closed | source executable | candidate executable | checker attempted | exact | mismatch | candidate execution failed | unsupported |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CONS | 27 | 27 | 0 | 27 | 27 | 27 | 25 | 2 | 0 | 0 |
| LONGTAIL | 18 | 18 | 0 | 18 | 18 | 18 | 12 | 6 | 0 | 0 |
| PERF | 48 | 48 | 0 | 48 | 47 | 47 | 43 | 4 | 1 | 0 |
| PORT | 27 | 6 | 21 | 5 | 3 | 3 | 1 | 2 | 2 | 1 |

PORT remains the main fail-closed / execution-failure frontier. CONS, LONGTAIL,
and PERF all generated candidates for every planned row, but still include
strict checker mismatches and one Spark candidate execution failure.
