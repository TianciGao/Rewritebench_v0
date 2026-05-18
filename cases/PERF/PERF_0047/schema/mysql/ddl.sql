-- PERF_0047 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (
    ss_sold_date_sk int,
    ss_store_sk int,
    ss_net_profit decimal(9,2)
);

create table date_dim (
    d_date_sk int primary key,
    d_month_seq int
);

create table store (
    s_store_sk int primary key,
    s_state varchar(2),
    s_county varchar(30)
);
