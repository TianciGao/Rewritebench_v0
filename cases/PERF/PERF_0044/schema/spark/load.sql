-- PERF_0044 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim (d_date_sk, d_year) values
    (1, 2001);

insert into item (i_item_sk, i_category, i_class) values
    (10, 'Books', 'Reference');

insert into store (s_store_sk, s_state) values
    (20, 'TN');

insert into store_sales (
    ss_sold_date_sk,
    ss_item_sk,
    ss_store_sk,
    ss_net_profit,
    ss_ext_sales_price
) values
    (1, 10, 20, 15.00, 100.00);
