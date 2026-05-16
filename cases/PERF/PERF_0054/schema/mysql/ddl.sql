-- PERF_0054 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table date_dim (
  d_date_sk int,
  d_year int,
  d_moy int
);

create table store_sales (
  ss_sold_date_sk int,
  ss_item_sk int,
  ss_ext_sales_price decimal(9,2)
);

create table item (
  i_item_sk int,
  i_brand_id int,
  i_brand varchar(255),
  i_manufact_id int
);
