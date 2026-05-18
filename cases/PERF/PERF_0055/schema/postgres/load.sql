insert into customer values
  (1, 'CUST_Q4', 'Ada', 'Jones', 'Y', 'UNITED STATES', 'adaj', 'ada@example.test');
insert into date_dim values
  (200101, 2001),
  (200201, 2002);
insert into store_sales values
  (1, 200101, 20.00, 10.00, 0.00, 10.00),
  (1, 200201, 40.00, 20.00, 0.00, 20.00);
insert into catalog_sales values
  (1, 200101, 20.00, 10.00, 0.00, 10.00),
  (1, 200201, 80.00, 40.00, 0.00, 40.00);
insert into web_sales values
  (1, 200101, 20.00, 10.00, 0.00, 10.00),
  (1, 200201, 30.00, 15.00, 0.00, 15.00);
