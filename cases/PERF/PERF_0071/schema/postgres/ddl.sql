create table store_sales (
  ss_sold_date_sk integer not null,
  ss_item_sk integer not null,
  ss_store_sk integer not null,
  ss_customer_sk integer not null,
  ss_ticket_number integer not null,
  ss_net_profit numeric(12,2) not null
);

create table store_returns (
  sr_returned_date_sk integer not null,
  sr_item_sk integer not null,
  sr_customer_sk integer not null,
  sr_ticket_number integer not null,
  sr_net_loss numeric(12,2) not null
);

create table catalog_sales (
  cs_sold_date_sk integer not null,
  cs_item_sk integer not null,
  cs_bill_customer_sk integer not null,
  cs_net_profit numeric(12,2) not null
);

create table date_dim (
  d_date_sk integer primary key,
  d_year integer not null,
  d_moy integer not null,
  d_date date not null
);

create table store (
  s_store_sk integer primary key,
  s_store_id text not null,
  s_store_name text not null
);

create table item (
  i_item_sk integer primary key,
  i_item_id text not null,
  i_item_desc text not null
);
