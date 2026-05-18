-- PERF_0066 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, 11, 1999);
insert into item values (20, 300, 'Brand-300', 400, 'Manufact-400', 7);
insert into customer_address values (30, '12345');
insert into customer values (40, 30);
insert into store values (50, '54321');
insert into store_sales values (1, 20, 40, 50, 99.00);
