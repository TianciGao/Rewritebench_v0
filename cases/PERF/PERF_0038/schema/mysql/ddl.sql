-- PERF_0038 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table customer (
    c_customer_sk int primary key,
    c_current_addr_sk int,
    c_current_cdemo_sk int
);

create table customer_address (
    ca_address_sk int primary key,
    ca_county varchar(80)
);

create table customer_demographics (
    cd_demo_sk int primary key,
    cd_gender varchar(1),
    cd_marital_status varchar(1),
    cd_education_status varchar(30),
    cd_purchase_estimate int,
    cd_credit_rating varchar(30),
    cd_dep_count int,
    cd_dep_employed_count int,
    cd_dep_college_count int
);

create table date_dim (
    d_date_sk int primary key,
    d_year int,
    d_moy int
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
