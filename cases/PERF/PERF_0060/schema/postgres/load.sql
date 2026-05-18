insert into date_dim (d_date_sk, d_year) values (1, 2001), (2, 2002);
insert into customer (c_customer_sk, c_customer_id, c_first_name, c_last_name, c_preferred_cust_flag, c_birth_country, c_login, c_email_address)
values (10, 'CUST-10', 'Ada', 'Lovelace', 'Y', 'USA', 'ada', 'ada@example.test');
insert into store_sales (ss_customer_sk, ss_sold_date_sk, ss_ext_list_price, ss_ext_discount_amt) values
  (10, 1, 100.00, 0.00),
  (10, 2, 150.00, 0.00);
insert into web_sales (ws_bill_customer_sk, ws_sold_date_sk, ws_ext_list_price, ws_ext_discount_amt) values
  (10, 1, 100.00, 0.00),
  (10, 2, 300.00, 0.00);
