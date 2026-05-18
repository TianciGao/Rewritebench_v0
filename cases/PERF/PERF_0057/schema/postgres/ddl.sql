create table store_sales (
  ss_sold_date_sk integer,
  ss_item_sk integer,
  ss_cdemo_sk integer,
  ss_promo_sk integer,
  ss_quantity integer,
  ss_list_price numeric,
  ss_coupon_amt numeric,
  ss_sales_price numeric
);

create table customer_demographics (
  cd_demo_sk integer primary key,
  cd_gender text,
  cd_marital_status text,
  cd_education_status text
);

create table date_dim (
  d_date_sk integer primary key,
  d_year integer
);

create table item (
  i_item_sk integer primary key,
  i_item_id text
);

create table promotion (
  p_promo_sk integer primary key,
  p_channel_email text,
  p_channel_event text
);
