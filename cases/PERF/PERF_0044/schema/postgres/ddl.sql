create table store_sales (ss_sold_date_sk integer, ss_item_sk integer, ss_store_sk integer, ss_net_profit decimal(9,2), ss_ext_sales_price decimal(9,2));
create table date_dim (d_date_sk integer primary key, d_year integer);
create table item (i_item_sk integer primary key, i_category varchar(30), i_class varchar(30));
create table store (s_store_sk integer primary key, s_state varchar(2));
