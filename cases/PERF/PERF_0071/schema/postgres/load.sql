insert into date_dim (d_date_sk, d_year, d_moy, d_date) values
  (251, 2000, 4, date '2000-04-10'),
  (252, 2000, 5, date '2000-05-05'),
  (253, 2000, 5, date '2000-05-15');

insert into store (s_store_sk, s_store_id, s_store_name) values
  (25, 'STORE-25', 'Witness Store');

insert into item (i_item_sk, i_item_id, i_item_desc) values
  (2501, 'ITEM-2501', 'Witness item');

insert into store_sales (ss_sold_date_sk, ss_item_sk, ss_store_sk, ss_customer_sk, ss_ticket_number, ss_net_profit) values
  (251, 2501, 25, 900, 9001, 100.00);

insert into store_returns (sr_returned_date_sk, sr_item_sk, sr_customer_sk, sr_ticket_number, sr_net_loss) values
  (252, 2501, 900, 9001, 5.00);

insert into catalog_sales (cs_sold_date_sk, cs_item_sk, cs_bill_customer_sk, cs_net_profit) values
  (253, 2501, 900, 30.00);
