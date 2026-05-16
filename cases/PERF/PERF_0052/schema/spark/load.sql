-- PERF_0052 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, 2000);
insert into store values (10, 'TN');
insert into customer values (101, 'CUST_A'), (102, 'CUST_B');
insert into store_returns values
  (101, 10, 1, 200.00),
  (102, 10, 1, 10.00);
