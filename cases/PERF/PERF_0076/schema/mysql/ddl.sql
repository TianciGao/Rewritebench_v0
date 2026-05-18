-- PERF_0076 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (
  ss_sold_date_sk int not null,
  ss_addr_sk int not null,
  ss_ext_sales_price decimal(12,2) not null
);

create table web_sales (
  ws_sold_date_sk int not null,
  ws_bill_addr_sk int not null,
  ws_ext_sales_price decimal(12,2) not null
);

create table date_dim (
  d_date_sk int primary key,
  d_qoy int not null,
  d_year int not null
);

create table customer_address (
  ca_address_sk int primary key,
  ca_county varchar(255) not null
);
