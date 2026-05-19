-- PERF_0033 minimal Spark SQL schema for referenced columns only.

create table date_dim
(
    d_date_sk int,
    d_moy int,
    d_year int
);

create table item
(
    i_item_sk int,
    i_manager_id int,
    i_brand_id int,
    i_brand string
);

create table store_sales
(
    ss_sold_date_sk int,
    ss_item_sk int,
    ss_ext_sales_price decimal(9, 2)
);
