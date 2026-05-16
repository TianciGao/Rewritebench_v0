-- PERF_0062 minimal Spark SQL schema for referenced columns only.

create table store_sales (
  ss_store_sk int,
  ss_sold_date_sk int,
  ss_cdemo_sk int,
  ss_hdemo_sk int,
  ss_addr_sk int,
  ss_quantity int,
  ss_ext_sales_price decimal(9, 2),
  ss_ext_wholesale_cost decimal(9, 2),
  ss_sales_price decimal(9, 2),
  ss_net_profit decimal(9, 2)
);

create table store (
  s_store_sk int
);

create table customer_demographics (
  cd_demo_sk int,
  cd_marital_status string,
  cd_education_status string
);

create table household_demographics (
  hd_demo_sk int,
  hd_dep_count int
);

create table customer_address (
  ca_address_sk int,
  ca_country string,
  ca_state string
);

create table date_dim (
  d_date_sk int,
  d_year int
);
