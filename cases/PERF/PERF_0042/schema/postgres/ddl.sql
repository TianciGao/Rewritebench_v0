create table store_sales (
    ss_sold_date_sk integer,
    ss_item_sk integer,
    ss_store_sk integer,
    ss_cdemo_sk integer,
    ss_quantity integer,
    ss_list_price decimal(9,2),
    ss_coupon_amt decimal(9,2),
    ss_sales_price decimal(9,2)
);

create table customer_demographics (
    cd_demo_sk integer primary key,
    cd_gender varchar(1),
    cd_marital_status varchar(1),
    cd_education_status varchar(30)
);

create table date_dim (
    d_date_sk integer primary key,
    d_year integer
);

create table store (
    s_store_sk integer primary key,
    s_state varchar(2)
);

create table item (
    i_item_sk integer primary key,
    i_item_id varchar(30)
);
