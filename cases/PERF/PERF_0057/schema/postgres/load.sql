insert into date_dim (d_date_sk, d_year) values (1, 1998);
insert into item (i_item_sk, i_item_id) values (10, 'ITEM-10');
insert into customer_demographics (cd_demo_sk, cd_gender, cd_marital_status, cd_education_status)
values (20, 'F', 'W', 'Primary');
insert into promotion (p_promo_sk, p_channel_email, p_channel_event) values (30, 'N', 'Y');
insert into store_sales (ss_sold_date_sk, ss_item_sk, ss_cdemo_sk, ss_promo_sk, ss_quantity, ss_list_price, ss_coupon_amt, ss_sales_price)
values (1, 10, 20, 30, 3, 20.00, 1.00, 18.00);
