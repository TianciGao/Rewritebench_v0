create table store_sales (
    ss_sold_date_sk integer,
    ss_store_sk integer,
    ss_net_profit decimal(9,2)
);

create table date_dim (
    d_date_sk integer primary key,
    d_month_seq integer
);

create table store (
    s_store_sk integer primary key,
    s_state varchar(2),
    s_county varchar(30)
);
