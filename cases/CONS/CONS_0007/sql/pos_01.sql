SELECT e1.*
FROM tmp_emps e1
JOIN (
  SELECT DISTINCT e2.commission
  FROM tmp_emps e2
  JOIN tmp_emps e3
    ON e2.commission = e3.commission
   AND e2.deptno <> e3.deptno
) AS good_commissions
  ON e1.commission = good_commissions.commission;
