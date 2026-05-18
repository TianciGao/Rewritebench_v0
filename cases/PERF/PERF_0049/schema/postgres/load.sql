insert into date_dim (d_date_sk, d_date) values (1, date '1998-08-04');

insert into store (s_store_sk, s_store_id) values (10, 'S80A');
insert into item (i_item_sk, i_current_price) values (20, 75.00);
insert into promotion (p_promo_sk, p_channel_tv) values (30, 'N');

insert into store_sales (
    ss_sold_date_sk,
    ss_store_sk,
    ss_item_sk,
    ss_promo_sk,
    ss_ticket_number,
    ss_ext_sales_price,
    ss_net_profit
) values
    (1, 10, 20, 30, 1001, 150.00, 40.00);
