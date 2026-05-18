create table catalog_sales (
  cs_order_number integer,
  cs_warehouse_sk integer,
  cs_ship_date_sk integer,
  cs_ship_addr_sk integer,
  cs_call_center_sk integer,
  cs_ext_ship_cost numeric,
  cs_net_profit numeric
);

create table date_dim (
  d_date_sk integer primary key,
  d_date date
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_state text
);

create table call_center (
  cc_call_center_sk integer primary key,
  cc_county text
);

create table catalog_returns (
  cr_order_number integer
);
