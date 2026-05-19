INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno) VALUES
(1, 'ALICE', 'CLERK', NULL, DATE '2020-01-01', 1000.00, NULL, 10),
(2, 'BOB', 'CLERK', NULL, DATE '2020-01-02', 1000.00, NULL, 20),
(3, 'CAROL', 'MANAGER', NULL, DATE '2020-01-03', 2000.00, NULL, 10),
(4, 'DAVE', 'ANALYST', NULL, DATE '2020-01-04', 3000.00, NULL, 20);
INSERT INTO bonus (ename, job, sal, comm) VALUES
('X', 'CLERK', 0.00, 0.00),
('Y', 'MANAGER', 0.00, 0.00);
