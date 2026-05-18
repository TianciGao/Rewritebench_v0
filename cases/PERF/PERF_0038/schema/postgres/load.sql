insert into date_dim (d_date_sk, d_year, d_moy) values
    (1, 2002, 4);

insert into customer_address (ca_address_sk, ca_county) values
    (10, 'Walker County');

insert into customer_demographics (
    cd_demo_sk,
    cd_gender,
    cd_marital_status,
    cd_education_status,
    cd_purchase_estimate,
    cd_credit_rating,
    cd_dep_count,
    cd_dep_employed_count,
    cd_dep_college_count
) values
    (20, 'F', 'M', 'College', 5000, 'Good', 2, 1, 1);

insert into customer (c_customer_sk, c_current_addr_sk, c_current_cdemo_sk) values
    (100, 10, 20);

insert into store_sales (ss_customer_sk, ss_sold_date_sk) values
    (100, 1);

insert into web_sales (ws_bill_customer_sk, ws_sold_date_sk) values
    (100, 1);
