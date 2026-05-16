SELECT *
FROM t0
WHERE t0a < (
  SELECT SUM(c)
  FROM (
    SELECT t1c AS c
    FROM t1
    WHERE t1a = t0a
    UNION ALL
    SELECT t2c AS c
    FROM t2
    WHERE t2b = t0b
  ) AS tmp
);
