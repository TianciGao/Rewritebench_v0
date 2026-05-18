-- PERF_0036 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into item (i_item_sk, i_item_id) values
    (10, 'item_alpha');

insert into date_dim (d_date_sk, d_date, d_week_seq) values
    (1, '1998-02-19', 100),
    (2, '1998-02-20', 100);

insert into store_sales (ss_item_sk, ss_sold_date_sk, ss_ext_sales_price) values
    (10, 1, 100.00);

insert into catalog_sales (cs_item_sk, cs_sold_date_sk, cs_ext_sales_price) values
    (10, 1, 100.00);

insert into web_sales (ws_item_sk, ws_sold_date_sk, ws_ext_sales_price) values
    (10, 1, 100.00);
