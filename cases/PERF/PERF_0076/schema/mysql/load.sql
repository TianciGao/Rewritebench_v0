-- PERF_0076 draft MySQL witness data for package enablement review only.
-- Derived mechanically from validation/pg_witness_data.sql.
-- Draft only: do not treat as executed or validated.

insert into date_dim (d_date_sk, d_qoy, d_year) values
  (1, 1, 2000),
  (2, 2, 2000),
  (3, 3, 2000);

insert into customer_address (ca_address_sk, ca_county) values
  (1, 'Witness County');

insert into store_sales (ss_sold_date_sk, ss_addr_sk, ss_ext_sales_price) values
  (1, 1, 100.00),
  (2, 1, 110.00),
  (3, 1, 121.00);

insert into web_sales (ws_sold_date_sk, ws_bill_addr_sk, ws_ext_sales_price) values
  (1, 1, 100.00),
  (2, 1, 150.00),
  (3, 1, 240.00);
