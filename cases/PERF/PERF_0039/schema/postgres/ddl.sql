create table item (
    i_item_sk integer primary key,
    i_brand_id integer,
    i_class_id integer,
    i_category_id integer
);

create table date_dim (
    d_date_sk integer primary key,
    d_year integer,
    d_moy integer,
    d_dom integer,
    d_week_seq integer
);

create table store_sales (
    ss_item_sk integer,
    ss_sold_date_sk integer,
    ss_quantity integer,
    ss_list_price decimal(9,2)
);

create table catalog_sales (
    cs_item_sk integer,
    cs_sold_date_sk integer,
    cs_quantity integer,
    cs_list_price decimal(9,2)
);

create table web_sales (
    ws_item_sk integer,
    ws_sold_date_sk integer,
    ws_quantity integer,
    ws_list_price decimal(9,2)
);
