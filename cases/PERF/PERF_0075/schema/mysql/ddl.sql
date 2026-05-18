-- PERF_0075 draft MySQL schema for package enablement review only.
-- Derived mechanically from schema/ddl_pg.sql.
-- Draft only: do not treat as executed or validated.

create table web_returns (
  wr_returning_customer_sk int not null,
  wr_returned_date_sk int not null,
  wr_returning_addr_sk int not null,
  wr_return_amt decimal(12,2) not null
);

create table date_dim (
  d_date_sk int primary key,
  d_year int not null
);

create table customer_address (
  ca_address_sk int primary key,
  ca_state varchar(20) not null
);

create table customer (
  c_customer_sk int primary key,
  c_current_addr_sk int not null,
  c_customer_id varchar(255) not null,
  c_salutation varchar(20) not null,
  c_first_name varchar(255) not null,
  c_last_name varchar(255) not null,
  c_preferred_cust_flag varchar(5) not null,
  c_birth_day int not null,
  c_birth_month int not null,
  c_birth_year int not null,
  c_birth_country varchar(255) not null,
  c_login varchar(255) not null,
  c_email_address varchar(255) not null,
  c_last_review_date_sk int not null
);
