-- PERF_0035 minimal Spark SQL schema for referenced columns only.

create table item
(
    i_item_sk int,
    i_category string,
    i_brand string
);

create table catalog_sales
(
    cs_item_sk int,
    cs_sold_date_sk int,
    cs_call_center_sk int,
    cs_sales_price decimal(9, 2)
);

create table date_dim
(
    d_date_sk int,
    d_year int,
    d_moy int
);

create table call_center
(
    cc_call_center_sk int,
    cc_name string
);
