-- PERF_0072 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table catalog_sales (
  cs_item_sk int not null,
  cs_sold_date_sk int not null,
  cs_bill_cdemo_sk int not null,
  cs_promo_sk int not null,
  cs_quantity decimal(12,2) not null,
  cs_list_price decimal(12,2) not null,
  cs_coupon_amt decimal(12,2) not null,
  cs_sales_price decimal(12,2) not null
);

create table customer_demographics (
  cd_demo_sk int primary key,
  cd_gender varchar(20) not null,
  cd_marital_status varchar(20) not null,
  cd_education_status varchar(64) not null
);

create table date_dim (
  d_date_sk int primary key,
  d_year int not null
);

create table item (
  i_item_sk int primary key,
  i_item_id varchar(255) not null
);

create table promotion (
  p_promo_sk int primary key,
  p_channel_email varchar(5) not null,
  p_channel_event varchar(5) not null
);
