-- PERF_0065 minimal Spark SQL schema for referenced columns only.

create table store_sales (
  ss_sold_date_sk int,
  ss_item_sk int,
  ss_store_sk int,
  ss_customer_sk int,
  ss_ticket_number int,
  ss_quantity decimal(9, 2)
);

create table store_returns (
  sr_customer_sk int,
  sr_item_sk int,
  sr_ticket_number int,
  sr_returned_date_sk int,
  sr_return_quantity decimal(9, 2)
);

create table catalog_sales (
  cs_bill_customer_sk int,
  cs_item_sk int,
  cs_sold_date_sk int,
  cs_quantity decimal(9, 2)
);

create table date_dim (
  d_date_sk int,
  d_quarter_name string
);

create table store (
  s_store_sk int,
  s_state string
);

create table item (
  i_item_sk int,
  i_item_id string,
  i_item_desc string
);
