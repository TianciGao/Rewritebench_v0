-- PERF_0073 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It does not imply PostgreSQL/MySQL readiness.

insert into store_sales values (0, 12.00, 100.00, 10.00);
insert into store_sales values (6, 95.00, 10.00, 10.00);
insert into store_sales values (11, 70.00, 10.00, 10.00);
insert into store_sales values (16, 145.00, 10.00, 10.00);
insert into store_sales values (21, 140.00, 10.00, 10.00);
insert into store_sales values (26, 30.00, 10.00, 10.00);
