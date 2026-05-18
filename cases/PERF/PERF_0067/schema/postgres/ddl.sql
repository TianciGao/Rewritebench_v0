create table catalog_sales (
  cs_item_sk integer not null,
  cs_sold_date_sk integer not null,
  cs_ext_sales_price numeric(12,2) not null
);

create table item (
  i_item_sk integer primary key,
  i_item_id text not null,
  i_item_desc text not null,
  i_category text not null,
  i_class text not null,
  i_current_price numeric(12,2) not null
);

create table date_dim (
  d_date_sk integer primary key,
  d_date date not null
);
