create table date_dim (
  d_date_sk integer,
  d_year integer,
  d_moy integer
);
create table store_sales (
  ss_sold_date_sk integer,
  ss_item_sk integer,
  ss_ext_sales_price numeric
);
create table item (
  i_item_sk integer,
  i_brand_id integer,
  i_brand text,
  i_manufact_id integer
);
