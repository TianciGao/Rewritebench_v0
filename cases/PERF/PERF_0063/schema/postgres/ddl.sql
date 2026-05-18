create table catalog_sales (
  cs_bill_customer_sk integer,
  cs_sold_date_sk integer,
  cs_sales_price numeric
);

create table customer (
  c_customer_sk integer primary key,
  c_current_addr_sk integer
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_zip text,
  ca_state text
);

create table date_dim (
  d_date_sk integer primary key,
  d_qoy integer,
  d_year integer
);
