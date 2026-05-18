-- PERF_0038 source SQL.
-- Frozen from TPC-DS query_variants/query10a.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization replaces TOP 100 with LIMIT 100.

select
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    count(*) as cnt1,
    cd.cd_purchase_estimate,
    count(*) as cnt2,
    cd.cd_credit_rating,
    count(*) as cnt3,
    cd.cd_dep_count,
    count(*) as cnt4,
    cd.cd_dep_employed_count,
    count(*) as cnt5,
    cd.cd_dep_college_count,
    count(*) as cnt6
from customer c,
     customer_address ca,
     customer_demographics cd
where c.c_current_addr_sk = ca.ca_address_sk
  and ca.ca_county in ('Walker County', 'Richland County', 'Gaines County', 'Douglas County', 'Dona Ana County')
  and cd.cd_demo_sk = c.c_current_cdemo_sk
  and exists (
      select *
      from store_sales ss,
           date_dim d
      where c.c_customer_sk = ss.ss_customer_sk
        and ss.ss_sold_date_sk = d.d_date_sk
        and d.d_year = 2002
        and d.d_moy between 4 and 4 + 3
  )
  and exists (
      select *
      from (
          select ws.ws_bill_customer_sk as customer_sk, d.d_year, d.d_moy
          from web_sales ws,
               date_dim d
          where ws.ws_sold_date_sk = d.d_date_sk
            and d.d_year = 2002
            and d.d_moy between 4 and 4 + 3
          union all
          select cs.cs_ship_customer_sk as customer_sk, d.d_year, d.d_moy
          from catalog_sales cs,
               date_dim d
          where cs.cs_sold_date_sk = d.d_date_sk
            and d.d_year = 2002
            and d.d_moy between 4 and 4 + 3
      ) x
      where c.c_customer_sk = x.customer_sk
  )
group by
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    cd.cd_purchase_estimate,
    cd.cd_credit_rating,
    cd.cd_dep_count,
    cd.cd_dep_employed_count,
    cd.cd_dep_college_count
order by
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    cd.cd_purchase_estimate,
    cd.cd_credit_rating,
    cd.cd_dep_count,
    cd.cd_dep_employed_count,
    cd.cd_dep_college_count
limit 100;
