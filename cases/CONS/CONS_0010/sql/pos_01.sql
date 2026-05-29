SELECT e1.*
FROM emp e1
WHERE NOT (
  EXISTS (
    SELECT 1
    FROM emp e2
    WHERE e2.sal = e1.sal
      AND e2.empno <> e1.empno
  )
  AND EXISTS (
    SELECT 1
    FROM bonus b
    WHERE b.job = e1.job
  )
);
