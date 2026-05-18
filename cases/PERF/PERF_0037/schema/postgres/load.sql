insert into date_dim (d_date_sk, d_date) values
    (1, date '1998-08-04');

insert into store (s_store_sk, s_store_id) values
    (10, 'S1');

insert into catalog_page (cp_catalog_page_sk, cp_catalog_page_id) values
    (20, 'CP1');

insert into web_site (web_site_sk, web_site_id) values
    (30, 'WS1');

insert into store_sales (ss_store_sk, ss_sold_date_sk, ss_ext_sales_price, ss_net_profit) values
    (10, 1, 100.00, 30.00);

insert into catalog_sales (cs_catalog_page_sk, cs_sold_date_sk, cs_ext_sales_price, cs_net_profit) values
    (20, 1, 200.00, 50.00);

insert into web_sales (ws_web_site_sk, ws_sold_date_sk, ws_ext_sales_price, ws_net_profit, ws_item_sk, ws_order_number) values
    (30, 1, 300.00, 70.00, 1000, 1);
