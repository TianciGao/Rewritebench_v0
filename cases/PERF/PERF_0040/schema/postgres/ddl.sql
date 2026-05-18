create table catalog_sales (
    cs_sold_date_sk integer,
    cs_item_sk integer,
    cs_bill_cdemo_sk integer,
    cs_bill_customer_sk integer,
    cs_quantity integer,
    cs_list_price decimal(9,2),
    cs_coupon_amt decimal(9,2),
    cs_sales_price decimal(9,2),
    cs_net_profit decimal(9,2)
);

create table customer_demographics (
    cd_demo_sk integer primary key,
    cd_gender varchar(1),
    cd_education_status varchar(30),
    cd_dep_count integer
);

create table customer (
    c_customer_sk integer primary key,
    c_current_cdemo_sk integer,
    c_current_addr_sk integer,
    c_birth_month integer,
    c_birth_year integer
);

create table customer_address (
    ca_address_sk integer primary key,
    ca_country varchar(30),
    ca_state varchar(10),
    ca_county varchar(80)
);

create table date_dim (
    d_date_sk integer primary key,
    d_year integer
);

create table item (
    i_item_sk integer primary key,
    i_item_id varchar(30)
);
