-- draft_id: JOB_DRAFT_0005
-- intended divergence: similar shape but intentionally altered predicate or join condition
-- not official case
-- Proposed hard negative: change one equality literal to a related but different value. This rewrite is intentionally semantically different from the source query.
SELECT min(t.title) AS typical_european_movie
FROM company_type AS ct
JOIN movie_companies AS mc ON ct.id = mc.company_type_id
JOIN movie_info AS mi ON mc.movie_id = mi.movie_id
JOIN title AS t ON t.id = mi.movie_id AND t.id = mc.movie_id
CROSS JOIN info_type AS it
WHERE ct.kind = 'distributors'
  AND mc.note like '%(theatrical)%'
  AND mc.note like '%(France)%'
  AND mi.info IN ('Sweden', 'Norway', 'Germany', 'Denmark', 'Swedish', 'Denish', 'Norwegian', 'German')
  AND t.production_year > 2005
  AND it.id = mi.info_type_id;
;
