insert into customer_address (ca_address_sk, ca_state, ca_zip, ca_country) values
  (1, 'TX', '12345', 'usa');

insert into customer (c_customer_sk, c_first_name, c_last_name, c_current_addr_sk, c_birth_country) values
  (700, 'Market', 'Customer', 1, 'Canada');

insert into store (s_store_sk, s_store_name, s_state, s_zip, s_market_id) values
  (70, 'Market Store', 'TX', '12345', 7);

insert into item (i_item_sk, i_color, i_current_price, i_manager_id, i_units, i_size) values
  (2401, 'orchid', 11.00, 1, 'Each', 'Small'),
  (2402, 'chiffon', 12.00, 1, 'Each', 'Small');

insert into store_sales (ss_ticket_number, ss_item_sk, ss_customer_sk, ss_store_sk, ss_sales_price) values
  (7001, 2401, 700, 70, 100.00),
  (7002, 2402, 700, 70, 80.00);

insert into store_returns (sr_ticket_number, sr_item_sk) values
  (7001, 2401),
  (7002, 2402);
