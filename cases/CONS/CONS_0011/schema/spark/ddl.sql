CREATE TABLE emp (empno INT, ename STRING, job STRING, mgr INT, hiredate DATE, sal DECIMAL(10,2), comm DECIMAL(10,2), deptno INT) USING parquet;
CREATE TABLE dept (deptno INT, dname STRING, loc STRING) USING parquet;
CREATE TABLE bonus (ename STRING, job STRING, sal DECIMAL(10,2), comm DECIMAL(10,2)) USING parquet;
