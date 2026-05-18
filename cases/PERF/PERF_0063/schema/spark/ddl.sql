-- PERF_0063 minimal Spark SQL schema for referenced columns only.

create table catalog_sales (
  cs_bill_customer_sk int,
  cs_sold_date_sk int,
  cs_sales_price decimal(9, 2)
);

create table customer (
  c_customer_sk int,
  c_current_addr_sk int
);

create table customer_address (
  ca_address_sk int,
  ca_zip string,
  ca_state string
);

create table date_dim (
  d_date_sk int,
  d_qoy int,
  d_year int
);
