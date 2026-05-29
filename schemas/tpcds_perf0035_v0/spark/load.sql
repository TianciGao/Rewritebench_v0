-- PERF_0035 minimal Spark witness data.
-- This is a deliberately tiny case-local dataset for Spark validation only.
-- It is not a TPC-DS scale dataset and does not imply PostgreSQL/MySQL readiness.

insert into item (i_item_sk, i_category, i_brand) values
    (10, 'Books', 'brand_alpha');

insert into call_center (cc_call_center_sk, cc_name) values
    (100, 'cc_alpha');

insert into date_dim (d_date_sk, d_year, d_moy) values
    (1, 1999, 12),
    (2, 2000, 1),
    (3, 2000, 2),
    (4, 2001, 1);

insert into catalog_sales (cs_item_sk, cs_sold_date_sk, cs_call_center_sk, cs_sales_price) values
    (10, 1, 100, 100.00),
    (10, 2, 100, 100.00),
    (10, 3, 100, 200.00),
    (10, 4, 100, 200.00);
