-- PERF_0047 minimal Spark SQL schema for referenced columns only.

create table store_sales (
    ss_sold_date_sk int,
    ss_store_sk int,
    ss_net_profit decimal(9, 2)
);

create table date_dim (
    d_date_sk int,
    d_month_seq int
);

create table store (
    s_store_sk int,
    s_state string,
    s_county string
);
