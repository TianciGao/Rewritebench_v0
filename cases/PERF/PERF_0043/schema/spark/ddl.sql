-- PERF_0043 minimal Spark SQL schema for referenced columns only.

create table customer (
    c_customer_sk int,
    c_current_addr_sk int,
    c_current_cdemo_sk int
);

create table customer_address (
    ca_address_sk int,
    ca_state string
);

create table customer_demographics (
    cd_demo_sk int,
    cd_gender string,
    cd_marital_status string,
    cd_dep_count int,
    cd_dep_employed_count int,
    cd_dep_college_count int
);

create table date_dim (
    d_date_sk int,
    d_year int,
    d_qoy int
);

create table store_sales (
    ss_customer_sk int,
    ss_sold_date_sk int
);

create table web_sales (
    ws_bill_customer_sk int,
    ws_sold_date_sk int
);

create table catalog_sales (
    cs_ship_customer_sk int,
    cs_sold_date_sk int
);
