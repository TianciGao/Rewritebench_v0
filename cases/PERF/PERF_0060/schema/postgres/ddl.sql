create table customer (
  c_customer_sk integer primary key,
  c_customer_id text,
  c_first_name text,
  c_last_name text,
  c_preferred_cust_flag text,
  c_birth_country text,
  c_login text,
  c_email_address text
);

create table store_sales (
  ss_customer_sk integer,
  ss_sold_date_sk integer,
  ss_ext_list_price numeric,
  ss_ext_discount_amt numeric
);

create table web_sales (
  ws_bill_customer_sk integer,
  ws_sold_date_sk integer,
  ws_ext_list_price numeric,
  ws_ext_discount_amt numeric
);

create table date_dim (
  d_date_sk integer primary key,
  d_year integer
);
