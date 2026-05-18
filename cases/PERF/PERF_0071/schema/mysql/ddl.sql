-- PERF_0071 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (
  ss_sold_date_sk int not null,
  ss_item_sk int not null,
  ss_store_sk int not null,
  ss_customer_sk int not null,
  ss_ticket_number int not null,
  ss_net_profit decimal(12,2) not null
);

create table store_returns (
  sr_returned_date_sk int not null,
  sr_item_sk int not null,
  sr_customer_sk int not null,
  sr_ticket_number int not null,
  sr_net_loss decimal(12,2) not null
);

create table catalog_sales (
  cs_sold_date_sk int not null,
  cs_item_sk int not null,
  cs_bill_customer_sk int not null,
  cs_net_profit decimal(12,2) not null
);

create table date_dim (
  d_date_sk int primary key,
  d_year int not null,
  d_moy int not null,
  d_date date not null
);

create table store (
  s_store_sk int primary key,
  s_store_id varchar(255) not null,
  s_store_name varchar(255) not null
);

create table item (
  i_item_sk int primary key,
  i_item_id varchar(255) not null,
  i_item_desc varchar(255) not null
);
