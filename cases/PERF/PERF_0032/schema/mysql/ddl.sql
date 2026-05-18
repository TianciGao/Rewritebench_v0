-- PERF_0032 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table catalog_sales
(
    cs_sold_date_sk int,
    cs_bill_customer_sk int,
    cs_item_sk int
);

create table web_sales
(
    ws_sold_date_sk int,
    ws_bill_customer_sk int,
    ws_item_sk int
);

create table item
(
    i_item_sk int primary key,
    i_category varchar(50),
    i_class varchar(50)
);

create table date_dim
(
    d_date_sk int primary key,
    d_moy int,
    d_year int,
    d_month_seq int
);

create table customer
(
    c_customer_sk int primary key,
    c_current_addr_sk int
);

create table store_sales
(
    ss_sold_date_sk int,
    ss_customer_sk int,
    ss_ext_sales_price decimal(9,2)
);

create table customer_address
(
    ca_address_sk int primary key,
    ca_county varchar(50),
    ca_state varchar(20)
);

create table store
(
    s_county varchar(50),
    s_state varchar(20)
);
