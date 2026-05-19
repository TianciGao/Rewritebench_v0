-- PERF_0035 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table item
(
    i_item_sk int primary key,
    i_category varchar(50),
    i_brand varchar(50)
);

create table catalog_sales
(
    cs_item_sk int,
    cs_sold_date_sk int,
    cs_call_center_sk int,
    cs_sales_price decimal(9,2)
);

create table date_dim
(
    d_date_sk int primary key,
    d_year int,
    d_moy int
);

create table call_center
(
    cc_call_center_sk int primary key,
    cc_name varchar(50)
);
