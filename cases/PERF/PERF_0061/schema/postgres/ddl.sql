create table web_sales (
  ws_item_sk integer,
  ws_sold_date_sk integer,
  ws_ext_sales_price numeric
);

create table item (
  i_item_sk integer primary key,
  i_item_id text,
  i_item_desc text,
  i_category text,
  i_class text,
  i_current_price numeric
);

create table date_dim (
  d_date_sk integer primary key,
  d_date date
);
