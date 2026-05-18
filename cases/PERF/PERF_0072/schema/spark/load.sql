-- PERF_0072 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It does not imply PostgreSQL/MySQL readiness.

insert into customer_demographics values (1, 'F', 'W', 'Primary');
insert into date_dim values (1, 1998);
insert into item values (10, 'ITEM-10');
insert into promotion values (100, 'N', 'N');

insert into catalog_sales values (10, 1, 1, 100, 4.00, 20.00, 2.00, 18.00);
