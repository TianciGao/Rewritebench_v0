-- PERF_0062 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (
  ss_store_sk int,
  ss_sold_date_sk int,
  ss_cdemo_sk int,
  ss_hdemo_sk int,
  ss_addr_sk int,
  ss_quantity int,
  ss_ext_sales_price decimal(9,2),
  ss_ext_wholesale_cost decimal(9,2),
  ss_sales_price decimal(9,2),
  ss_net_profit decimal(9,2)
);

create table store (
  s_store_sk int primary key
);

create table customer_demographics (
  cd_demo_sk int primary key,
  cd_marital_status varchar(20),
  cd_education_status varchar(50)
);

create table household_demographics (
  hd_demo_sk int primary key,
  hd_dep_count int
);

create table customer_address (
  ca_address_sk int primary key,
  ca_country varchar(50),
  ca_state varchar(20)
);

create table date_dim (
  d_date_sk int primary key,
  d_year int
);
