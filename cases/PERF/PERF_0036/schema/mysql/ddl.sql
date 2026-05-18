-- PERF_0036 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table item
(
    i_item_sk int primary key,
    i_item_id varchar(50)
);

create table date_dim
(
    d_date_sk int primary key,
    d_date date,
    d_week_seq int
);

create table store_sales
(
    ss_item_sk int,
    ss_sold_date_sk int,
    ss_ext_sales_price decimal(9,2)
);

create table catalog_sales
(
    cs_item_sk int,
    cs_sold_date_sk int,
    cs_ext_sales_price decimal(9,2)
);

create table web_sales
(
    ws_item_sk int,
    ws_sold_date_sk int,
    ws_ext_sales_price decimal(9,2)
);
