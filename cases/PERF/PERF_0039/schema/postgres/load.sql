insert into item (i_item_sk, i_brand_id, i_class_id, i_category_id) values
    (10, 1, 2, 3);

insert into date_dim (d_date_sk, d_year, d_moy, d_dom, d_week_seq) values
    (1, 2000, 11, 1, 200011),
    (2, 1999, 12, 16, 19991216),
    (3, 1998, 12, 16, 19981216);

insert into store_sales (ss_item_sk, ss_sold_date_sk, ss_quantity, ss_list_price) values
    (10, 1, 10, 10.00),
    (10, 1, 10, 10.00),
    (10, 2, 20, 10.00),
    (10, 3, 20, 10.00);

insert into catalog_sales (cs_item_sk, cs_sold_date_sk, cs_quantity, cs_list_price) values
    (10, 1, 10, 10.00),
    (10, 1, 10, 10.00);

insert into web_sales (ws_item_sk, ws_sold_date_sk, ws_quantity, ws_list_price) values
    (10, 1, 10, 10.00),
    (10, 1, 10, 10.00);
