-- PERF_0072 minimal Spark SQL schema for referenced columns only.

create table catalog_sales (
  cs_item_sk int,
  cs_sold_date_sk int,
  cs_bill_cdemo_sk int,
  cs_promo_sk int,
  cs_quantity decimal(12, 2),
  cs_list_price decimal(12, 2),
  cs_coupon_amt decimal(12, 2),
  cs_sales_price decimal(12, 2)
);

create table customer_demographics (
  cd_demo_sk int,
  cd_gender string,
  cd_marital_status string,
  cd_education_status string
);

create table date_dim (
  d_date_sk int,
  d_year int
);

create table item (
  i_item_sk int,
  i_item_id string
);

create table promotion (
  p_promo_sk int,
  p_channel_email string,
  p_channel_event string
);
