# Timing Readiness

Exact-gated timing is ready as the next diagnostic task for the 81 rows that
were exact/result-consistent in this execution/checker run.

Timing-eligible rows:

- PostgreSQL: 25
- MySQL: 26
- Spark: 30
- Overall: 81

Rows that must not be timed:

- 21 no-candidate rows.
- 14 checker mismatch rows.
- 3 candidate execution failure rows.
- 1 unsupported source-role / target-reference row.

Timing must remain exact-gated and local-only. It must not compute canonical
metrics by itself and must not update paper reports/results.
