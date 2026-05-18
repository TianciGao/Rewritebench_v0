create table store_sales (
    ss_sold_date_sk integer,
    ss_store_sk integer,
    ss_sales_price decimal(9,2)
);

create table date_dim (
    d_date_sk integer primary key,
    d_week_seq integer,
    d_month_seq integer,
    d_day_name varchar(10)
);

create table store (
    s_store_sk integer primary key,
    s_store_name varchar(40),
    s_store_id varchar(20)
);
