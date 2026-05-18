create table customer (
  c_customer_sk integer,
  c_customer_id text,
  c_first_name text,
  c_last_name text,
  c_preferred_cust_flag text,
  c_birth_country text,
  c_login text,
  c_email_address text
);
create table date_dim (
  d_date_sk integer,
  d_year integer
);
create table store_sales (
  ss_customer_sk integer,
  ss_sold_date_sk integer,
  ss_ext_list_price numeric,
  ss_ext_wholesale_cost numeric,
  ss_ext_discount_amt numeric,
  ss_ext_sales_price numeric
);
create table catalog_sales (
  cs_bill_customer_sk integer,
  cs_sold_date_sk integer,
  cs_ext_list_price numeric,
  cs_ext_wholesale_cost numeric,
  cs_ext_discount_amt numeric,
  cs_ext_sales_price numeric
);
create table web_sales (
  ws_bill_customer_sk integer,
  ws_sold_date_sk integer,
  ws_ext_list_price numeric,
  ws_ext_wholesale_cost numeric,
  ws_ext_discount_amt numeric,
  ws_ext_sales_price numeric
);
