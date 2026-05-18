-- PERF_0032 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim (d_date_sk, d_moy, d_year, d_month_seq) values
    (1, 3, 1999, 24003),
    (2, 4, 1999, 24004),
    (3, 5, 1999, 24005),
    (4, 6, 1999, 24006);

insert into item (i_item_sk, i_category, i_class) values
    (10, 'Jewelry', 'consignment');

insert into customer (c_customer_sk, c_current_addr_sk) values
    (100, 500),
    (200, 600);

insert into customer_address (ca_address_sk, ca_county, ca_state) values
    (500, 'King', 'WA'),
    (600, 'King', 'WA');

insert into store (s_county, s_state) values
    ('King', 'WA');

insert into catalog_sales (cs_sold_date_sk, cs_bill_customer_sk, cs_item_sk) values
    (1, 100, 10);

insert into web_sales (ws_sold_date_sk, ws_bill_customer_sk, ws_item_sk) values
    (1, 200, 10);

insert into store_sales (ss_sold_date_sk, ss_customer_sk, ss_ext_sales_price) values
    (2, 100, 150.00),
    (2, 200, 50.00);
