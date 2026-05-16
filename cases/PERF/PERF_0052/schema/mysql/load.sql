-- PERF_0052 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim values (1, 2000);
insert into store values (10, 'TN');
insert into customer values (101, 'CUST_A'), (102, 'CUST_B');
insert into store_returns values
  (101, 10, 1, 200.00),
  (102, 10, 1, 10.00);
