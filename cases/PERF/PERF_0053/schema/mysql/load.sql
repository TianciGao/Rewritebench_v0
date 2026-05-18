-- PERF_0053 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim values
  (1, 100, 'Sunday', 2001),
  (2, 153, 'Sunday', 2002);

insert into web_sales values
  (1, 200.00),
  (2, 100.00);
