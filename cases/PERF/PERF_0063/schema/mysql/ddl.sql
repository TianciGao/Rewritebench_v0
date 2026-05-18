-- PERF_0063 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table catalog_sales (
  cs_bill_customer_sk int,
  cs_sold_date_sk int,
  cs_sales_price decimal(9,2)
);

create table customer (
  c_customer_sk int primary key,
  c_current_addr_sk int
);

create table customer_address (
  ca_address_sk int primary key,
  ca_zip varchar(20),
  ca_state varchar(2)
);

create table date_dim (
  d_date_sk int primary key,
  d_qoy int,
  d_year int
);
