-- PERF_0076 minimal Spark SQL schema for referenced columns only.

create table store_sales (
  ss_sold_date_sk int,
  ss_addr_sk int,
  ss_ext_sales_price decimal(12, 2)
);

create table web_sales (
  ws_sold_date_sk int,
  ws_bill_addr_sk int,
  ws_ext_sales_price decimal(12, 2)
);

create table date_dim (
  d_date_sk int,
  d_qoy int,
  d_year int
);

create table customer_address (
  ca_address_sk int,
  ca_county string
);
