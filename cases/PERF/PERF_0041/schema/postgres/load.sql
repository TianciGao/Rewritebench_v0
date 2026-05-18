insert into date_dim (d_date_sk, d_month_seq) values
    (1, 1212);

insert into item (i_item_sk, i_product_name, i_brand, i_class, i_category) values
    (10, 'Product 10', 'Brand 10', 'Class 10', 'Category 10');

insert into warehouse (w_warehouse_sk) values
    (20);

insert into inventory (inv_date_sk, inv_item_sk, inv_warehouse_sk, inv_quantity_on_hand) values
    (1, 10, 20, 50);
