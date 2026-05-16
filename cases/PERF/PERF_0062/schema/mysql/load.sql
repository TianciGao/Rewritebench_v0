-- PERF_0062 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into store values (1);
insert into date_dim values (1, 2001);
insert into customer_demographics values (10, 'D', '2 yr Degree');
insert into household_demographics values (20, 3);
insert into customer_address values (30, 'United States', 'CO');
insert into store_sales values (1, 1, 10, 20, 30, 4, 120.00, 80.00, 125.00, 150.00);
