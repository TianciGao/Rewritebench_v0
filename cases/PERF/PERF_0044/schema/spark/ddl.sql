-- PERF_0044 minimal Spark SQL schema for referenced columns only.

create table store_sales (
    ss_sold_date_sk int,
    ss_item_sk int,
    ss_store_sk int,
    ss_net_profit decimal(9, 2),
    ss_ext_sales_price decimal(9, 2)
);

create table date_dim (
    d_date_sk int,
    d_year int
);

create table item (
    i_item_sk int,
    i_category string,
    i_class string
);

create table store (
    s_store_sk int,
    s_state string
);
