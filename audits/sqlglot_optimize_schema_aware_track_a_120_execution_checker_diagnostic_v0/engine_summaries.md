# Engine Summaries

| engine | planned | selected | generated | fail-closed | source executable | candidate executable | checker attempted | exact | mismatch | source exec failed | candidate exec failed | no candidate | unsupported |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PostgreSQL | 40 | 40 | 34 | 6 | 34 | 32 | 32 | 29 | 3 | 0 | 2 | 6 | 0 |
| MySQL | 40 | 40 | 32 | 8 | 40 | 29 | 29 | 20 | 9 | 0 | 3 | 8 | 0 |
| Spark | 40 | 40 | 39 | 6 | 34 | 30 | 30 | 17 | 13 | 0 | 4 | 1 | 5 |

## Overall

| field | value |
|---|---:|
| planned rows | 120 |
| selected rows | 120 |
| candidate generated rows | 105 |
| fail-closed rows | 20 |
| source executable rows | 108 |
| candidate executable rows | 91 |
| checker attempted rows | 91 |
| exact/result-consistent rows | 66 |
| mismatch rows | 25 |
| source execution failed rows | 0 |
| candidate execution failed rows | 9 |
| no-candidate rows | 15 |
| unsupported rows | 5 |

MySQL source execution includes source-only execution for explicit MySQL fail-closed rows. PostgreSQL/Spark generation-failed or unsupported rows remained fail-closed and did not receive candidate execution.
