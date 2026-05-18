-- PERF_0065 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, '1998Q1');
insert into date_dim values (2, '1998Q2');
insert into date_dim values (3, '1998Q3');
insert into store values (10, 'TN');
insert into item values (20, 'ITEM-20', 'Witness item');
insert into store_sales values (1, 20, 10, 100, 5000, 4.00);
insert into store_returns values (100, 20, 5000, 2, 1.00);
insert into catalog_sales values (100, 20, 3, 7.00);
