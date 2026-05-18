create table web_sales (
    ws_sold_date_sk integer,
    ws_item_sk integer,
    ws_net_paid decimal(9,2)
);

create table date_dim (
    d_date_sk integer primary key,
    d_month_seq integer
);

create table item (
    i_item_sk integer primary key,
    i_category varchar(30),
    i_class varchar(30)
);
