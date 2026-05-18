-- PERF_0063 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim values (1, 2, 2000);
insert into customer_address values (10, '85669', 'TX');
insert into customer values (100, 10);
insert into catalog_sales values (100, 1, 42.00);
