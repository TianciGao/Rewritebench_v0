insert into item (i_item_sk, i_item_id, i_item_desc, i_category, i_class, i_current_price) values
  (2001, 'ITEM-2001', 'Minimal jewelry witness item', 'Jewelry', 'class-a', 42.00);

insert into date_dim (d_date_sk, d_date) values
  (101, date '2001-01-15');

insert into catalog_sales (cs_item_sk, cs_sold_date_sk, cs_ext_sales_price) values
  (2001, 101, 100.00);
