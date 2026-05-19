insert into item (i_item_sk, i_item_id, i_color) values
    (10, 'item_orchid', 'orchid'),
    (20, 'item_lace', 'lace');

insert into date_dim (d_date_sk, d_year, d_moy) values
    (1, 2000, 1);

insert into customer_address (ca_address_sk, ca_gmt_offset) values
    (100, -8),
    (200, -7);

insert into store_sales (ss_item_sk, ss_sold_date_sk, ss_addr_sk, ss_ext_sales_price) values
    (10, 1, 100, 100.00),
    (20, 1, 100, 50.00);

insert into catalog_sales (cs_item_sk, cs_sold_date_sk, cs_bill_addr_sk, cs_ext_sales_price) values
    (10, 1, 100, 200.00);

insert into web_sales (ws_item_sk, ws_sold_date_sk, ws_bill_addr_sk, ws_ext_sales_price) values
    (10, 1, 100, 300.00);
