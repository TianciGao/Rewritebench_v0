-- PERF_0066 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table date_dim (
  d_date_sk int primary key,
  d_moy int,
  d_year int
);

create table store_sales (
  ss_sold_date_sk int,
  ss_item_sk int,
  ss_customer_sk int,
  ss_store_sk int,
  ss_ext_sales_price decimal(9,2)
);

create table item (
  i_item_sk int primary key,
  i_brand_id int,
  i_brand varchar(255),
  i_manufact_id int,
  i_manufact varchar(255),
  i_manager_id int
);

create table customer (
  c_customer_sk int primary key,
  c_current_addr_sk int
);

create table customer_address (
  ca_address_sk int primary key,
  ca_zip varchar(20)
);

create table store (
  s_store_sk int primary key,
  s_zip varchar(20)
);
