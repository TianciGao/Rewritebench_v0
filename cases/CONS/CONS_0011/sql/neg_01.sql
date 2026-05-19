SELECT e1.ename
FROM emp e1
WHERE (
  SELECT COUNT(*)
  FROM dept d
  JOIN bonus b
    ON d.dname = b.ename
   AND b.job = e1.job
) > 0;
