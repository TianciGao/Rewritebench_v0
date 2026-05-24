# Engine Summaries

| engine | selected | generated | fail-closed | source executable | candidate executable | checker attempted | exact | mismatch | candidate execution failed | unsupported |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PostgreSQL | 40 | 33 | 7 | 33 | 32 | 32 | 25 | 7 | 1 | 0 |
| MySQL | 40 | 33 | 7 | 33 | 33 | 33 | 26 | 7 | 0 | 0 |
| Spark | 40 | 33 | 7 | 32 | 30 | 30 | 30 | 0 | 2 | 1 |
| Overall | 120 | 99 | 21 | 98 | 95 | 95 | 81 | 14 | 3 | 1 |

Candidate origin counts:

| engine | calcite_rel_to_sql | calcite_parse_only | no_candidate |
|---|---:|---:|---:|
| PostgreSQL | 29 | 4 | 7 |
| MySQL | 25 | 8 | 7 |
| Spark | 4 | 29 | 7 |
| Overall | 58 | 41 | 21 |

Failure bucket counts:

| engine | none | mismatch | no_candidate_sql | candidate_execution_failed | unsupported_engine |
|---|---:|---:|---:|---:|---:|
| PostgreSQL | 25 | 7 | 7 | 1 | 0 |
| MySQL | 26 | 7 | 7 | 0 | 0 |
| Spark | 30 | 0 | 7 | 2 | 1 |
| Overall | 81 | 14 | 21 | 3 | 1 |

MySQL/Spark target-dialect mode behaved as expected in this run: 33 candidates
were generated per engine, and no MySQL/Spark candidate was blocked by the
PostgreSQL-dialect guard.
