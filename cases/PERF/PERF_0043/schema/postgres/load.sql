insert into date_dim (d_date_sk, d_year, d_qoy) values (1, 1999, 2);
insert into customer_address (ca_address_sk, ca_state) values (10, 'TN');
insert into customer_demographics (cd_demo_sk, cd_gender, cd_marital_status, cd_dep_count, cd_dep_employed_count, cd_dep_college_count) values (20, 'F', 'W', 2, 1, 1);
insert into customer (c_customer_sk, c_current_addr_sk, c_current_cdemo_sk) values (100, 10, 20);
insert into store_sales (ss_customer_sk, ss_sold_date_sk) values (100, 1);
insert into web_sales (ws_bill_customer_sk, ws_sold_date_sk) values (100, 1);
