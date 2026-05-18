-- PERF_0073 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (
  ss_quantity int not null,
  ss_list_price decimal(12,2) not null,
  ss_coupon_amt decimal(12,2) not null,
  ss_wholesale_cost decimal(12,2) not null
);
