insert into date_dim (d_date_sk, d_year) values
  (1, 2002);

insert into customer_address (ca_address_sk, ca_state) values
  (1, 'IL'),
  (2, 'IL'),
  (3, 'IL');

insert into customer (
  c_customer_sk, c_current_addr_sk, c_customer_id, c_salutation, c_first_name,
  c_last_name, c_preferred_cust_flag, c_birth_day, c_birth_month, c_birth_year,
  c_birth_country, c_login, c_email_address, c_last_review_date_sk
) values
  (1, 1, 'CUST-001', 'Ms.', 'Alice', 'High', 'Y', 1, 1, 1980, 'USA', 'alice', 'alice@example.com', 10),
  (2, 2, 'CUST-002', 'Mr.', 'Bob', 'Mid', 'N', 2, 2, 1981, 'USA', 'bob', 'bob@example.com', 11),
  (3, 3, 'CUST-003', 'Ms.', 'Cara', 'Low', 'Y', 3, 3, 1982, 'USA', 'cara', 'cara@example.com', 12);

insert into web_returns (wr_returning_customer_sk, wr_returned_date_sk, wr_returning_addr_sk, wr_return_amt) values
  (1, 1, 1, 100.00),
  (2, 1, 2, 40.00),
  (3, 1, 3, 40.00);
