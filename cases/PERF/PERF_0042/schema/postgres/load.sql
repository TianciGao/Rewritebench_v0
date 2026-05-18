insert into date_dim (d_date_sk, d_year) values (1, 1998);

insert into item (i_item_sk, i_item_id) values (10, 'ITEM27A');

insert into store (s_store_sk, s_state) values (20, 'TN');

insert into customer_demographics (cd_demo_sk, cd_gender, cd_marital_status, cd_education_status) values
    (30, 'F', 'W', 'Primary');

insert into store_sales (
    ss_sold_date_sk,
    ss_item_sk,
    ss_store_sk,
    ss_cdemo_sk,
    ss_quantity,
    ss_list_price,
    ss_coupon_amt,
    ss_sales_price
) values
    (1, 10, 20, 30, 4, 20.00, 1.00, 79.00);
