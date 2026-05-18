insert into date_dim (d_date_sk, d_month_seq) values (1, 1212);

insert into item (i_item_sk, i_category, i_class) values (10, 'Books', 'Reference');

insert into web_sales (ws_sold_date_sk, ws_item_sk, ws_net_paid) values
    (1, 10, 90.00);
