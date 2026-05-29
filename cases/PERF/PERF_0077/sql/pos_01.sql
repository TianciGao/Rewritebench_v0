-- case_id: PERF_0077
-- intended equivalence: explicit inner-join normalization only; no intended semantic change
-- draft_origin: JOB_DRAFT_0003
SELECT min(t.title) AS movie_title
FROM movie_info AS mi
JOIN movie_keyword AS mk ON mk.movie_id = mi.movie_id
JOIN keyword AS k ON k.id = mk.keyword_id
JOIN title AS t ON t.id = mi.movie_id AND t.id = mk.movie_id
WHERE k.keyword like '%sequel%'
  AND mi.info IN ('Sweden', 'Norway', 'Germany', 'Denmark', 'Swedish', 'Denish', 'Norwegian', 'German')
  AND t.production_year > 2005;
