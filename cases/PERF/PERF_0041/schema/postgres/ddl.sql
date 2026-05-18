create table inventory (
    inv_date_sk integer,
    inv_item_sk integer,
    inv_warehouse_sk integer,
    inv_quantity_on_hand integer
);

create table date_dim (
    d_date_sk integer primary key,
    d_month_seq integer
);

create table item (
    i_item_sk integer primary key,
    i_product_name varchar(80),
    i_brand varchar(80),
    i_class varchar(80),
    i_category varchar(80)
);

create table warehouse (
    w_warehouse_sk integer primary key
);
