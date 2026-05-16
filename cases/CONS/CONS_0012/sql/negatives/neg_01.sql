SELECT d.*
FROM dept d
JOIN (
  SELECT deptno
  FROM emp
  GROUP BY deptno
  HAVING COUNT(*) >= 2
) AS enough_rows
  ON enough_rows.deptno = d.deptno;
