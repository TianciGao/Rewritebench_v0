SELECT t1.i, t1.j
FROM table1 AS t1
WHERE NOT EXISTS (
  SELECT 1
  FROM table2 AS t2
  WHERE t2.j = t1.i
    AND t2.i = t1.j
);
