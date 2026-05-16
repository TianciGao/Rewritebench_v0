-- PERF_0034 minimal Spark SQL schema for referenced columns only.

create table item (
    i_item_sk int,
    i_item_id string,
    i_color string
);

create table date_dim (
    d_date_sk int,
    d_year int,
    d_moy int
);

create table customer_address (
    ca_address_sk int,
    ca_gmt_offset int
);

create table store_sales (
    ss_item_sk int,
    ss_sold_date_sk int,
    ss_addr_sk int,
    ss_ext_sales_price decimal(9, 2)
);

create table catalog_sales (
    cs_item_sk int,
    cs_sold_date_sk int,
    cs_bill_addr_sk int,
    cs_ext_sales_price decimal(9, 2)
);

create table web_sales (
    ws_item_sk int,
    ws_sold_date_sk int,
    ws_bill_addr_sk int,
    ws_ext_sales_price decimal(9, 2)
);
