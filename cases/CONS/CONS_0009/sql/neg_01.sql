SELECT t0.t0a, t0.t0b
FROM t0
LEFT JOIN (SELECT t1a, SUM(t1c) AS sum_t1c FROM t1 GROUP BY t1a) AS s1
  ON s1.t1a = t0.t0a
LEFT JOIN (SELECT t2a, SUM(t2c) AS sum_t2c FROM t2 GROUP BY t2a) AS s2
  ON s2.t2a = t0.t0a
WHERE t0.t0a < CASE
                  WHEN s1.sum_t1c IS NULL AND s2.sum_t2c IS NULL THEN NULL
                  ELSE COALESCE(s1.sum_t1c, 0) + COALESCE(s2.sum_t2c, 0)
                END;
