SELECT *
FROM tmp_emps e1
WHERE EXISTS (
  SELECT *
  FROM (
    SELECT e2.deptno
    FROM tmp_emps e2
    WHERE e2.commission = e1.commission
  ) AS table3
  WHERE table3.deptno <> e1.deptno
);
