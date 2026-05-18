create table store_sales (
  ss_sold_date_sk integer not null,
  ss_item_sk integer not null,
  ss_customer_sk integer not null,
  ss_quantity numeric(12,2) not null,
  ss_sales_price numeric(12,2) not null
);

create table date_dim (
  d_date_sk integer primary key,
  d_year integer not null,
  d_moy integer not null,
  d_date date not null
);

create table item (
  i_item_sk integer primary key,
  i_item_desc text not null
);

create table customer (
  c_customer_sk integer primary key,
  c_last_name text not null,
  c_first_name text not null
);

create table catalog_sales (
  cs_quantity numeric(12,2) not null,
  cs_list_price numeric(12,2) not null,
  cs_sold_date_sk integer not null,
  cs_item_sk integer not null,
  cs_bill_customer_sk integer not null
);

create table web_sales (
  ws_quantity numeric(12,2) not null,
  ws_list_price numeric(12,2) not null,
  ws_sold_date_sk integer not null,
  ws_item_sk integer not null,
  ws_bill_customer_sk integer not null
);
