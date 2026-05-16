-- PERF_0056 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table customer_address (
  ca_address_sk int,
  ca_state varchar(20)
);

create table customer (
  c_customer_sk int,
  c_current_addr_sk int
);

create table store_sales (
  ss_customer_sk int,
  ss_sold_date_sk int,
  ss_item_sk int
);

create table date_dim (
  d_date_sk int,
  d_year int,
  d_moy int,
  d_month_seq int
);

create table item (
  i_item_sk int,
  i_current_price decimal(9,2),
  i_category varchar(255)
);
