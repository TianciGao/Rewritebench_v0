-- PERF_0050 minimal Spark SQL schema for referenced columns only.

create table web_sales (
    ws_sold_date_sk int,
    ws_item_sk int,
    ws_net_paid decimal(9, 2)
);

create table date_dim (
    d_date_sk int,
    d_month_seq int
);

create table item (
    i_item_sk int,
    i_category string,
    i_class string
);
