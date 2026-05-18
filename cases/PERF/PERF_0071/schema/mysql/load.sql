-- PERF_0071 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim values (1, 2000, 4, '2000-04-10');
insert into date_dim values (2, 2000, 5, '2000-05-12');
insert into date_dim values (3, 2000, 6, '2000-06-20');
insert into date_dim values (4, 2001, 4, '2001-04-10');

insert into store values (10, 'S-10', 'Witness Store');
insert into item values (20, 'ITEM-20', 'Witness Item');

insert into store_sales values (1, 20, 10, 100, 5000, 12.00);
insert into store_returns values (2, 20, 100, 5000, 3.00);
insert into catalog_sales values (3, 20, 100, 8.00);
