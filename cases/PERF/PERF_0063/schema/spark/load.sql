-- PERF_0063 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, 2, 2000);
insert into customer_address values (10, '85669', 'TX');
insert into customer values (100, 10);
insert into catalog_sales values (100, 1, 42.00);
