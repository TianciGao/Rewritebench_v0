# Source/Candidate Diff

Source SQL:

- `cases/LONGTAIL/LONGTAIL_0023/sql/source.sql`

Candidate SQL:

- `runs/user/common_core_pg_noop_db_checker/candidate_sql/LONGTAIL_0023__postgres.sql`

Byte-level comparison:

- Source bytes: 776
- Candidate bytes: 776
- Source SHA-256: `758d318d64074b7bad77fdb1bc5418f9a87058603922d710161549eb43ebe926`
- Candidate SHA-256: `758d318d64074b7bad77fdb1bc5418f9a87058603922d710161549eb43ebe926`
- Byte-identical: yes

`diff -u` result:

- No differences.

SQL-shape notes:

- Uses two CTEs: `OutboundLinks` and `InboundLinks`.
- Both CTEs aggregate `PostLinks` with `COUNT(*)`.
- Main query uses two `LEFT JOIN`s, `COALESCE`, an arithmetic `total_links` expression, `WHERE total_links > 0`, and `ORDER BY total_links DESC, p.Id`.

Conclusion:

- No formatting, quoting, alias, projection, grouping, aggregation, CTE, order, or limit change exists between source and candidate.
- `likely_candidate_semantic_drift` is not supported by the source/candidate diff.
