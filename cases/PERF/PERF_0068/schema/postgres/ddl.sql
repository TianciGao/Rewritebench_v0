create table inventory (
  inv_item_sk integer not null,
  inv_warehouse_sk integer not null,
  inv_date_sk integer not null,
  inv_quantity_on_hand numeric(12,2) not null
);

create table warehouse (
  w_warehouse_sk integer primary key,
  w_warehouse_name text not null
);

create table item (
  i_item_sk integer primary key,
  i_item_id text not null,
  i_current_price numeric(12,2) not null
);

create table date_dim (
  d_date_sk integer primary key,
  d_date date not null
);
