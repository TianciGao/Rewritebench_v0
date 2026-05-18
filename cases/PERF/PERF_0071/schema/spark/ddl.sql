-- PERF_0071 minimal Spark SQL schema for referenced columns only.

create table store_sales (
  ss_sold_date_sk int,
  ss_item_sk int,
  ss_store_sk int,
  ss_customer_sk int,
  ss_ticket_number int,
  ss_net_profit decimal(12, 2)
);

create table store_returns (
  sr_returned_date_sk int,
  sr_item_sk int,
  sr_customer_sk int,
  sr_ticket_number int,
  sr_net_loss decimal(12, 2)
);

create table catalog_sales (
  cs_sold_date_sk int,
  cs_item_sk int,
  cs_bill_customer_sk int,
  cs_net_profit decimal(12, 2)
);

create table date_dim (
  d_date_sk int,
  d_year int,
  d_moy int,
  d_date date
);

create table store (
  s_store_sk int,
  s_store_id string,
  s_store_name string
);

create table item (
  i_item_sk int,
  i_item_id string,
  i_item_desc string
);
