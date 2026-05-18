insert into date_dim (d_date_sk, d_week_seq, d_month_seq, d_day_name) values
    (1, 10, 1185, 'Sunday'),
    (2, 62, 1197, 'Sunday');

insert into store (s_store_sk, s_store_name, s_store_id) values
    (10, 'Store59', 'S59');

insert into store_sales (ss_sold_date_sk, ss_store_sk, ss_sales_price) values
    (1, 10, 100.00),
    (2, 10, 50.00);
