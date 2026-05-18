insert into date_dim (d_date_sk, d_date) values (1, date '2001-01-15');
insert into item (i_item_sk, i_item_id, i_item_desc, i_category, i_class, i_current_price)
values (10, 'ITEM-10', 'Witness item', 'Jewelry', 'Class-A', 12.34);
insert into web_sales (ws_item_sk, ws_sold_date_sk, ws_ext_sales_price) values (10, 1, 50.00);
