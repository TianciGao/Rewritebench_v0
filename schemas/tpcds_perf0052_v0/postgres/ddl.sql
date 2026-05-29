create table store_returns (
  sr_customer_sk integer,
  sr_store_sk integer,
  sr_returned_date_sk integer,
  sr_fee numeric
);
create table date_dim (
  d_date_sk integer,
  d_year integer
);
create table store (
  s_store_sk integer,
  s_state text
);
create table customer (
  c_customer_sk integer,
  c_customer_id text
);
