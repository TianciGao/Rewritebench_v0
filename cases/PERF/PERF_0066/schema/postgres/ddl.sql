create table date_dim (
  d_date_sk integer primary key,
  d_moy integer,
  d_year integer
);

create table store_sales (
  ss_sold_date_sk integer,
  ss_item_sk integer,
  ss_customer_sk integer,
  ss_store_sk integer,
  ss_ext_sales_price numeric
);

create table item (
  i_item_sk integer primary key,
  i_brand_id integer,
  i_brand text,
  i_manufact_id integer,
  i_manufact text,
  i_manager_id integer
);

create table customer (
  c_customer_sk integer primary key,
  c_current_addr_sk integer
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_zip text
);

create table store (
  s_store_sk integer primary key,
  s_zip text
);
