-- PERF_0065 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (
  ss_sold_date_sk int,
  ss_item_sk int,
  ss_store_sk int,
  ss_customer_sk int,
  ss_ticket_number int,
  ss_quantity decimal(9,2)
);

create table store_returns (
  sr_customer_sk int,
  sr_item_sk int,
  sr_ticket_number int,
  sr_returned_date_sk int,
  sr_return_quantity decimal(9,2)
);

create table catalog_sales (
  cs_bill_customer_sk int,
  cs_item_sk int,
  cs_sold_date_sk int,
  cs_quantity decimal(9,2)
);

create table date_dim (
  d_date_sk int primary key,
  d_quarter_name varchar(20)
);

create table store (
  s_store_sk int primary key,
  s_state varchar(20)
);

create table item (
  i_item_sk int primary key,
  i_item_id varchar(255),
  i_item_desc varchar(255)
);
