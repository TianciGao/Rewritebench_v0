SELECT *
FROM tmp_emps e1
WHERE EXISTS (
  SELECT 1
  FROM tmp_emps e2
  WHERE e2.commission = e1.commission
);
