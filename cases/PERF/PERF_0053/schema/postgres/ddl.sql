create table web_sales (
  ws_sold_date_sk integer,
  ws_ext_sales_price numeric
);
create table catalog_sales (
  cs_sold_date_sk integer,
  cs_ext_sales_price numeric
);
create table date_dim (
  d_date_sk integer,
  d_week_seq integer,
  d_day_name text,
  d_year integer
);
