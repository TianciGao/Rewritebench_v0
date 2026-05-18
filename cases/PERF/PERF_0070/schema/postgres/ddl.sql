create table store_sales (
  ss_ticket_number integer not null,
  ss_item_sk integer not null,
  ss_customer_sk integer not null,
  ss_store_sk integer not null,
  ss_sales_price numeric(12,2) not null
);

create table store_returns (
  sr_ticket_number integer not null,
  sr_item_sk integer not null
);

create table store (
  s_store_sk integer primary key,
  s_store_name text not null,
  s_state text not null,
  s_zip text not null,
  s_market_id integer not null
);

create table item (
  i_item_sk integer primary key,
  i_color text not null,
  i_current_price numeric(12,2) not null,
  i_manager_id integer not null,
  i_units text not null,
  i_size text not null
);

create table customer (
  c_customer_sk integer primary key,
  c_first_name text not null,
  c_last_name text not null,
  c_current_addr_sk integer not null,
  c_birth_country text not null
);

create table customer_address (
  ca_address_sk integer primary key,
  ca_state text not null,
  ca_zip text not null,
  ca_country text not null
);
