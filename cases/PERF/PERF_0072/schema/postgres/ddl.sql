create table catalog_sales (
  cs_item_sk integer not null,
  cs_sold_date_sk integer not null,
  cs_bill_cdemo_sk integer not null,
  cs_promo_sk integer not null,
  cs_quantity numeric(12,2) not null,
  cs_list_price numeric(12,2) not null,
  cs_coupon_amt numeric(12,2) not null,
  cs_sales_price numeric(12,2) not null
);

create table customer_demographics (
  cd_demo_sk integer primary key,
  cd_gender text not null,
  cd_marital_status text not null,
  cd_education_status text not null
);

create table date_dim (
  d_date_sk integer primary key,
  d_year integer not null
);

create table item (
  i_item_sk integer primary key,
  i_item_id text not null
);

create table promotion (
  p_promo_sk integer primary key,
  p_channel_email text not null,
  p_channel_event text not null
);
