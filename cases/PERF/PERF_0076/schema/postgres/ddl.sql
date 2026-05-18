create table store_sales (
  ss_sold_date_sk integer not null,
  ss_addr_sk integer not null,
  ss_ext_sales_price numeric(12,2) not null
);

create table web_sales (
  ws_sold_date_sk integer not null,
  ws_bill_addr_sk integer not null,
  ws_ext_sales_price numeric(12,2) not null
);

create table date_dim (
  d_date_sk integer primary key,
  d_qoy integer not null,
  d_year integer not null
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_county text not null
);
