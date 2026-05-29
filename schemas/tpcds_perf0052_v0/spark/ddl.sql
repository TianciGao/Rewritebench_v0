-- PERF_0052 minimal Spark SQL schema for referenced columns only.

create table store_returns (
  sr_customer_sk int,
  sr_store_sk int,
  sr_returned_date_sk int,
  sr_fee decimal(9, 2)
);

create table date_dim (
  d_date_sk int,
  d_year int
);

create table store (
  s_store_sk int,
  s_state string
);

create table customer (
  c_customer_sk int,
  c_customer_id string
);
