insert into date_dim (d_date_sk, d_year, d_moy, d_date) values
  (2301, 1999, 1, date '1999-01-15');

insert into item (i_item_sk, i_item_desc) values
  (230, 'Minimal frequent item');

insert into customer (c_customer_sk, c_last_name, c_first_name) values
  (500, 'Customer', 'Best');

insert into store_sales (ss_sold_date_sk, ss_item_sk, ss_customer_sk, ss_quantity, ss_sales_price) values
  (2301, 230, 500, 1, 100.00),
  (2301, 230, 500, 1, 100.00),
  (2301, 230, 500, 1, 100.00),
  (2301, 230, 500, 1, 100.00),
  (2301, 230, 500, 1, 100.00);

insert into catalog_sales (cs_quantity, cs_list_price, cs_sold_date_sk, cs_item_sk, cs_bill_customer_sk) values
  (2, 30.00, 2301, 230, 500);

insert into web_sales (ws_quantity, ws_list_price, ws_sold_date_sk, ws_item_sk, ws_bill_customer_sk) values
  (1, 40.00, 2301, 230, 500);
