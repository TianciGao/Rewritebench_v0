create table store_sales (
  ss_sold_date_sk integer,
  ss_item_sk integer,
  ss_store_sk integer,
  ss_customer_sk integer,
  ss_ticket_number integer,
  ss_quantity numeric
);

create table store_returns (
  sr_customer_sk integer,
  sr_item_sk integer,
  sr_ticket_number integer,
  sr_returned_date_sk integer,
  sr_return_quantity numeric
);

create table catalog_sales (
  cs_bill_customer_sk integer,
  cs_item_sk integer,
  cs_sold_date_sk integer,
  cs_quantity numeric
);

create table date_dim (
  d_date_sk integer primary key,
  d_quarter_name text
);

create table store (
  s_store_sk integer primary key,
  s_state text
);

create table item (
  i_item_sk integer primary key,
  i_item_id text,
  i_item_desc text
);
