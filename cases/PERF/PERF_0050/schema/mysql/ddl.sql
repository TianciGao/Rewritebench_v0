-- PERF_0050 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table web_sales (
    ws_sold_date_sk int,
    ws_item_sk int,
    ws_net_paid decimal(9,2)
);

create table date_dim (
    d_date_sk int primary key,
    d_month_seq int
);

create table item (
    i_item_sk int primary key,
    i_category varchar(30),
    i_class varchar(30)
);
