-- PERF_0076 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, 1, 2000);
insert into date_dim values (2, 2, 2000);
insert into date_dim values (3, 3, 2000);

insert into customer_address values (1, 'Witness County');

insert into store_sales values (1, 1, 100.00);
insert into store_sales values (2, 1, 110.00);
insert into store_sales values (3, 1, 121.00);

insert into web_sales values (1, 1, 100.00);
insert into web_sales values (2, 1, 150.00);
insert into web_sales values (3, 1, 240.00);
