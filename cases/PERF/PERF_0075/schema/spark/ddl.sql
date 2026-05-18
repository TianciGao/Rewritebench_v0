-- PERF_0075 minimal Spark SQL schema for referenced columns only.

create table web_returns (
  wr_returning_customer_sk int,
  wr_returned_date_sk int,
  wr_returning_addr_sk int,
  wr_return_amt decimal(12, 2)
);

create table date_dim (
  d_date_sk int,
  d_year int
);

create table customer_address (
  ca_address_sk int,
  ca_state string
);

create table customer (
  c_customer_sk int,
  c_current_addr_sk int,
  c_customer_id string,
  c_salutation string,
  c_first_name string,
  c_last_name string,
  c_preferred_cust_flag string,
  c_birth_day int,
  c_birth_month int,
  c_birth_year int,
  c_birth_country string,
  c_login string,
  c_email_address string,
  c_last_review_date_sk int
);
