create table store_sales (
  ss_store_sk integer,
  ss_sold_date_sk integer,
  ss_cdemo_sk integer,
  ss_hdemo_sk integer,
  ss_addr_sk integer,
  ss_quantity integer,
  ss_ext_sales_price numeric,
  ss_ext_wholesale_cost numeric,
  ss_sales_price numeric,
  ss_net_profit numeric
);

create table store (
  s_store_sk integer primary key
);

create table customer_demographics (
  cd_demo_sk integer primary key,
  cd_marital_status text,
  cd_education_status text
);

create table household_demographics (
  hd_demo_sk integer primary key,
  hd_dep_count integer
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_country text,
  ca_state text
);

create table date_dim (
  d_date_sk integer primary key,
  d_year integer
);
