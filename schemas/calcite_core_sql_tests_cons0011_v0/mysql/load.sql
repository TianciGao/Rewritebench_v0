INSERT INTO emp (empno, ename, job, mgr, hiredate, sal, comm, deptno) VALUES
(1, 'ALICE', 'CLERK', NULL, '2020-01-01', 100.00, NULL, 10),
(2, 'BOB', 'MANAGER', NULL, '2020-01-02', 200.00, NULL, 20);
INSERT INTO dept (deptno, dname, loc) VALUES
(10, 'ACCOUNTING', 'NEW YORK'),
(20, 'SALES', 'CHICAGO');
INSERT INTO bonus (ename, job, sal, comm) VALUES
('ACCOUNTING', 'CLERK', 0.00, 0.00);
