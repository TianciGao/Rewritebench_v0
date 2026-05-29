create table item
(
    i_item_sk integer primary key,
    i_item_id varchar(50),
    i_color varchar(50)
);

create table date_dim
(
    d_date_sk integer primary key,
    d_year integer,
    d_moy integer
);

create table customer_address
(
    ca_address_sk integer primary key,
    ca_gmt_offset integer
);

create table store_sales
(
    ss_item_sk integer,
    ss_sold_date_sk integer,
    ss_addr_sk integer,
    ss_ext_sales_price decimal(9,2)
);

create table catalog_sales
(
    cs_item_sk integer,
    cs_sold_date_sk integer,
    cs_bill_addr_sk integer,
    cs_ext_sales_price decimal(9,2)
);

create table web_sales
(
    ws_item_sk integer,
    ws_sold_date_sk integer,
    ws_bill_addr_sk integer,
    ws_ext_sales_price decimal(9,2)
);
