create table store_sales (
  ss_store_sk integer,
  ss_sold_date_sk integer,
  ss_net_profit numeric
);

create table date_dim (
  d_date_sk integer primary key,
  d_qoy integer,
  d_year integer
);

create table store (
  s_store_sk integer primary key,
  s_store_name text,
  s_zip text
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_zip text
);

create table customer (
  c_customer_sk integer primary key,
  c_current_addr_sk integer,
  c_preferred_cust_flag text
);
