-- PERF_0053 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table web_sales (
  ws_sold_date_sk int,
  ws_ext_sales_price decimal(9,2)
);

create table catalog_sales (
  cs_sold_date_sk int,
  cs_ext_sales_price decimal(9,2)
);

create table date_dim (
  d_date_sk int,
  d_week_seq int,
  d_day_name varchar(20),
  d_year int
);
