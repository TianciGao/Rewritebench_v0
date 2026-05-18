create table web_returns (
  wr_returning_customer_sk integer not null,
  wr_returned_date_sk integer not null,
  wr_returning_addr_sk integer not null,
  wr_return_amt numeric(12,2) not null
);

create table date_dim (
  d_date_sk integer primary key,
  d_year integer not null
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_state text not null
);

create table customer (
  c_customer_sk integer primary key,
  c_current_addr_sk integer not null,
  c_customer_id text not null,
  c_salutation text not null,
  c_first_name text not null,
  c_last_name text not null,
  c_preferred_cust_flag text not null,
  c_birth_day integer not null,
  c_birth_month integer not null,
  c_birth_year integer not null,
  c_birth_country text not null,
  c_login text not null,
  c_email_address text not null,
  c_last_review_date_sk integer not null
);
