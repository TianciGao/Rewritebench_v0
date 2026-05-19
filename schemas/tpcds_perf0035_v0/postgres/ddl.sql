create table item
(
    i_item_sk integer primary key,
    i_category varchar(50),
    i_brand varchar(50)
);

create table catalog_sales
(
    cs_item_sk integer,
    cs_sold_date_sk integer,
    cs_call_center_sk integer,
    cs_sales_price decimal(9,2)
);

create table date_dim
(
    d_date_sk integer primary key,
    d_year integer,
    d_moy integer
);

create table call_center
(
    cc_call_center_sk integer primary key,
    cc_name varchar(50)
);
