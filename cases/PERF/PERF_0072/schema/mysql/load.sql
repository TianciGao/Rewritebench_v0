-- PERF_0072 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into customer_demographics values (1, 'F', 'W', 'Primary');
insert into date_dim values (1, 1998);
insert into item values (10, 'ITEM-10');
insert into promotion values (100, 'N', 'N');

insert into catalog_sales values (10, 1, 1, 100, 4.00, 20.00, 2.00, 18.00);
