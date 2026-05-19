-- PERF_0054 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, 2001, 12);
insert into item values (10, 700, 'Brand#700', 436);
insert into store_sales values (1, 10, 123.45);
