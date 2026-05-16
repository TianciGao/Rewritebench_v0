-- PERF_0033 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into date_dim (d_date_sk, d_moy, d_year) values
    (1, 12, 2001);

insert into item (i_item_sk, i_manager_id, i_brand_id, i_brand) values
    (10, 36, 360, 'brand_manager_36'),
    (20, 37, 370, 'brand_manager_37');

insert into store_sales (ss_sold_date_sk, ss_item_sk, ss_ext_sales_price) values
    (1, 10, 150.00),
    (1, 20, 80.00);
