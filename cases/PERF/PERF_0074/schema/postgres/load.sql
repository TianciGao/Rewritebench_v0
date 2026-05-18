insert into date_dim (d_date_sk, d_moy, d_year) values
  (1, 4, 1999),
  (2, 5, 1999),
  (3, 6, 2000);

insert into item (i_item_sk, i_item_id, i_item_desc) values
  (1, 'ITEM-29', 'Query 29 witness item');

insert into store (s_store_sk, s_store_id, s_store_name) values
  (1, 'STORE-29', 'Query 29 witness store');

insert into store_sales (ss_sold_date_sk, ss_item_sk, ss_store_sk, ss_customer_sk, ss_ticket_number, ss_quantity) values
  (1, 1, 1, 100, 9001, 3.00);

insert into store_returns (sr_returned_date_sk, sr_customer_sk, sr_item_sk, sr_ticket_number, sr_return_quantity) values
  (2, 100, 1, 9001, 1.00);

insert into catalog_sales (cs_sold_date_sk, cs_bill_customer_sk, cs_item_sk, cs_quantity) values
  (3, 100, 1, 2.00);
