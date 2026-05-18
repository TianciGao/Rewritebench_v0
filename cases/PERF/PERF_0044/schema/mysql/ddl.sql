-- PERF_0044 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table store_sales (ss_sold_date_sk int, ss_item_sk int, ss_store_sk int, ss_net_profit decimal(9,2), ss_ext_sales_price decimal(9,2));
create table date_dim (d_date_sk int primary key, d_year int);
create table item (i_item_sk int primary key, i_category varchar(30), i_class varchar(30));
create table store (s_store_sk int primary key, s_state varchar(2));
