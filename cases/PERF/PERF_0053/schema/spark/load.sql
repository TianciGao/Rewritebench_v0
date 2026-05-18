-- PERF_0053 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim values
  (1, 100, 'Sunday', 2001),
  (2, 153, 'Sunday', 2002);

insert into web_sales values
  (1, 200.00),
  (2, 100.00);
