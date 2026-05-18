-- PERF_0066 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim values (1, 11, 1999);
insert into item values (20, 300, 'Brand-300', 400, 'Manufact-400', 7);
insert into customer_address values (30, '12345');
insert into customer values (40, 30);
insert into store values (50, '54321');
insert into store_sales values (1, 20, 40, 50, 99.00);
