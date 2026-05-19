create table date_dim
(
    d_date_sk integer primary key,
    d_moy integer,
    d_year integer
);

create table item
(
    i_item_sk integer primary key,
    i_manager_id integer,
    i_brand_id integer,
    i_brand varchar(50)
);

create table store_sales
(
    ss_sold_date_sk integer,
    ss_item_sk integer,
    ss_ext_sales_price decimal(9,2)
);
