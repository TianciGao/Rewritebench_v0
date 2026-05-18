-- PERF_0074 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, 4, 1999);
insert into date_dim values (2, 5, 1999);
insert into date_dim values (3, 6, 1999);
insert into date_dim values (4, 4, 1998);

insert into store values (10, 'S-10', 'Witness Store');
insert into item values (20, 'ITEM-20', 'Witness Item');

insert into store_sales values (1, 20, 10, 100, 5000, 5.00);
insert into store_returns values (2, 100, 20, 5000, 2.00);
insert into catalog_sales values (3, 100, 20, 7.00);
