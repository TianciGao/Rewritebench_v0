# Non-Exact Frontier

The non-exact frontier contains 39 rows:

- 21 `no_candidate_sql`
- 14 checker mismatches
- 3 candidate execution failures
- 1 unsupported engine/source-role policy row

No-candidate rows:

- `PORT_0003`, `PORT_0004`, `PORT_0005`, `PORT_0008`, `PORT_0012`,
  `PORT_0022`, and `PORT_0025` on each of PostgreSQL, MySQL, and Spark.

Checker mismatches:

- PostgreSQL: `PERF_0035`, `PERF_0062`, `CONS_0036`,
  `LONGTAIL_0011`, `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`.
- MySQL: `PERF_0035`, `PERF_0062`, `CONS_0037`, `PORT_0013`,
  `PORT_0024`, `LONGTAIL_0012`, `LONGTAIL_0013`.
- Spark: none.

Candidate execution failures:

- PostgreSQL: `PORT_0013`.
- Spark: `PERF_0062`, `PORT_0013`.

Unsupported row:

- Spark: `PORT_0024`, blocked by local diagnostic target-reference/source-role
  policy.

Candidate origins in the frontier:

- `no_candidate`: 21 rows.
- `calcite_rel_to_sql`: mismatch and unsupported rows remain present.
- `calcite_parse_only`: includes several mismatch / candidate-failure rows and
  must remain visible rather than being treated as ordinary route success.
