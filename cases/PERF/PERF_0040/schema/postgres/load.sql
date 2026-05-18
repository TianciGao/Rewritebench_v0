insert into date_dim (d_date_sk, d_year) values
    (1, 2001);

insert into item (i_item_sk, i_item_id) values
    (10, 'ITEM10');

insert into customer_demographics (cd_demo_sk, cd_gender, cd_education_status, cd_dep_count) values
    (20, 'M', 'College', 2);

insert into customer_address (ca_address_sk, ca_country, ca_state, ca_county) values
    (30, 'United States', 'ND', 'Cass County');

insert into customer (c_customer_sk, c_current_cdemo_sk, c_current_addr_sk, c_birth_month, c_birth_year) values
    (100, 20, 30, 9, 1978);

insert into catalog_sales (
    cs_sold_date_sk,
    cs_item_sk,
    cs_bill_cdemo_sk,
    cs_bill_customer_sk,
    cs_quantity,
    cs_list_price,
    cs_coupon_amt,
    cs_sales_price,
    cs_net_profit
) values
    (1, 10, 20, 100, 4, 25.00, 1.00, 99.00, 15.00);
