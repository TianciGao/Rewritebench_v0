insert into customer_demographics (cd_demo_sk, cd_gender, cd_marital_status, cd_education_status) values
  (1, 'F', 'W', 'Primary');

insert into date_dim (d_date_sk, d_year) values
  (1, 1998);

insert into item (i_item_sk, i_item_id) values
  (1, 'ITEM-26');

insert into promotion (p_promo_sk, p_channel_email, p_channel_event) values
  (1, 'N', 'Y');

insert into catalog_sales (
  cs_item_sk, cs_sold_date_sk, cs_bill_cdemo_sk, cs_promo_sk,
  cs_quantity, cs_list_price, cs_coupon_amt, cs_sales_price
) values
  (1, 1, 1, 1, 2.00, 20.00, 1.00, 19.00);
