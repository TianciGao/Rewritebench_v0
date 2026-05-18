create table catalog_sales
(
    cs_sold_date_sk integer,
    cs_bill_customer_sk integer,
    cs_item_sk integer
);

create table web_sales
(
    ws_sold_date_sk integer,
    ws_bill_customer_sk integer,
    ws_item_sk integer
);

create table item
(
    i_item_sk integer primary key,
    i_category varchar(50),
    i_class varchar(50)
);

create table date_dim
(
    d_date_sk integer primary key,
    d_moy integer,
    d_year integer,
    d_month_seq integer
);

create table customer
(
    c_customer_sk integer primary key,
    c_current_addr_sk integer
);

create table store_sales
(
    ss_sold_date_sk integer,
    ss_customer_sk integer,
    ss_ext_sales_price decimal(9,2)
);

create table customer_address
(
    ca_address_sk integer primary key,
    ca_county varchar(50),
    ca_state varchar(20)
);

create table store
(
    s_county varchar(50),
    s_state varchar(20)
);
