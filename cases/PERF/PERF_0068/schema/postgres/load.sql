insert into warehouse (w_warehouse_sk, w_warehouse_name) values
  (1, 'Warehouse A');

insert into item (i_item_sk, i_item_id, i_current_price) values
  (2101, 'ITEM-2101', 1.20);

insert into date_dim (d_date_sk, d_date) values
  (201, date '1998-04-01'),
  (202, date '1998-04-10');

insert into inventory (inv_item_sk, inv_warehouse_sk, inv_date_sk, inv_quantity_on_hand) values
  (2101, 1, 201, 10.00),
  (2101, 1, 202, 10.00);
