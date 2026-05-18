-- PERF_0071 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It does not imply PostgreSQL/MySQL readiness.

insert into date_dim values (1, 2000, 4, date '2000-04-10');
insert into date_dim values (2, 2000, 5, date '2000-05-12');
insert into date_dim values (3, 2000, 6, date '2000-06-20');
insert into date_dim values (4, 2001, 4, date '2001-04-10');

insert into store values (10, 'S-10', 'Witness Store');
insert into item values (20, 'ITEM-20', 'Witness Item');

insert into store_sales values (1, 20, 10, 100, 5000, 12.00);
insert into store_returns values (2, 20, 100, 5000, 3.00);
insert into catalog_sales values (3, 20, 100, 8.00);
