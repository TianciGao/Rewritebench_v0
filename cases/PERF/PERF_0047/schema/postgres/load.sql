insert into date_dim (d_date_sk, d_month_seq) values (1, 1212);

insert into store (s_store_sk, s_state, s_county) values (10, 'TN', 'Knox County');

insert into store_sales (ss_sold_date_sk, ss_store_sk, ss_net_profit) values
    (1, 10, 120.00);
