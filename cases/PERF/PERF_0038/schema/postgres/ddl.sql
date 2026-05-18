create table customer (
    c_customer_sk integer primary key,
    c_current_addr_sk integer,
    c_current_cdemo_sk integer
);

create table customer_address (
    ca_address_sk integer primary key,
    ca_county varchar(80)
);

create table customer_demographics (
    cd_demo_sk integer primary key,
    cd_gender varchar(1),
    cd_marital_status varchar(1),
    cd_education_status varchar(30),
    cd_purchase_estimate integer,
    cd_credit_rating varchar(30),
    cd_dep_count integer,
    cd_dep_employed_count integer,
    cd_dep_college_count integer
);

create table date_dim (
    d_date_sk integer primary key,
    d_year integer,
    d_moy integer
);

create table store_sales (
    ss_customer_sk integer,
    ss_sold_date_sk integer
);

create table web_sales (
    ws_bill_customer_sk integer,
    ws_sold_date_sk integer
);

create table catalog_sales (
    cs_ship_customer_sk integer,
    cs_sold_date_sk integer
);
