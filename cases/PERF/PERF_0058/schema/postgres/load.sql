insert into date_dim (d_date_sk, d_qoy, d_year) values (1, 1, 2002);
insert into store (s_store_sk, s_store_name, s_zip) values (10, 'Store 10', '89400');
insert into store_sales (ss_store_sk, ss_sold_date_sk, ss_net_profit) values (10, 1, 42.00);
insert into customer_address (ca_address_sk, ca_zip) values
  (1, '89436'), (2, '89436'), (3, '89436'), (4, '89436'), (5, '89436'), (6, '89436'),
  (7, '89436'), (8, '89436'), (9, '89436'), (10, '89436'), (11, '89436');
insert into customer (c_customer_sk, c_current_addr_sk, c_preferred_cust_flag) values
  (1, 1, 'Y'), (2, 2, 'Y'), (3, 3, 'Y'), (4, 4, 'Y'), (5, 5, 'Y'), (6, 6, 'Y'),
  (7, 7, 'Y'), (8, 8, 'Y'), (9, 9, 'Y'), (10, 10, 'Y'), (11, 11, 'Y');
