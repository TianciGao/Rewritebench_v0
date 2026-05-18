create table web_sales (ws_item_sk integer, ws_sold_date_sk integer, ws_sales_price decimal(9,2));
create table store_sales (ss_item_sk integer, ss_sold_date_sk integer, ss_sales_price decimal(9,2));
create table date_dim (d_date_sk integer primary key, d_date date, d_month_seq integer);
