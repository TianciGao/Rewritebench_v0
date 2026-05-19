create table customer_address (
  ca_address_sk integer,
  ca_state text
);
create table customer (
  c_customer_sk integer,
  c_current_addr_sk integer
);
create table store_sales (
  ss_customer_sk integer,
  ss_sold_date_sk integer,
  ss_item_sk integer
);
create table date_dim (
  d_date_sk integer,
  d_year integer,
  d_moy integer,
  d_month_seq integer
);
create table item (
  i_item_sk integer,
  i_current_price numeric,
  i_category text
);
