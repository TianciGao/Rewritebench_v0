-- PERF_0066 minimal Spark SQL schema for referenced columns only.

create table date_dim (
  d_date_sk int,
  d_moy int,
  d_year int
);

create table store_sales (
  ss_sold_date_sk int,
  ss_item_sk int,
  ss_customer_sk int,
  ss_store_sk int,
  ss_ext_sales_price decimal(9, 2)
);

create table item (
  i_item_sk int,
  i_brand_id int,
  i_brand string,
  i_manufact_id int,
  i_manufact string,
  i_manager_id int
);

create table customer (
  c_customer_sk int,
  c_current_addr_sk int
);

create table customer_address (
  ca_address_sk int,
  ca_zip string
);

create table store (
  s_store_sk int,
  s_zip string
);
