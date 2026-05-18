-- PERF_0040 source SQL.
-- Frozen from TPC-DS query_variants/query18a.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization replaces TOP 100 with LIMIT 100.

with results as (
    select
        i.i_item_id,
        ca.ca_country,
        ca.ca_state,
        ca.ca_county,
        cast(cs.cs_quantity as decimal(12,2)) as agg1,
        cast(cs.cs_list_price as decimal(12,2)) as agg2,
        cast(cs.cs_coupon_amt as decimal(12,2)) as agg3,
        cast(cs.cs_sales_price as decimal(12,2)) as agg4,
        cast(cs.cs_net_profit as decimal(12,2)) as agg5,
        cast(c.c_birth_year as decimal(12,2)) as agg6,
        cast(cd1.cd_dep_count as decimal(12,2)) as agg7
    from catalog_sales cs,
         customer_demographics cd1,
         customer_demographics cd2,
         customer c,
         customer_address ca,
         date_dim d,
         item i
    where cs.cs_sold_date_sk = d.d_date_sk
      and cs.cs_item_sk = i.i_item_sk
      and cs.cs_bill_cdemo_sk = cd1.cd_demo_sk
      and cs.cs_bill_customer_sk = c.c_customer_sk
      and cd1.cd_gender = 'M'
      and cd1.cd_education_status = 'College'
      and c.c_current_cdemo_sk = cd2.cd_demo_sk
      and c.c_current_addr_sk = ca.ca_address_sk
      and c.c_birth_month in (9, 5, 12, 4, 1, 10)
      and d.d_year = 2001
      and ca.ca_state in ('ND', 'WI', 'AL', 'NC', 'OK', 'MS', 'TN')
)
select
    i_item_id,
    ca_country,
    ca_state,
    ca_county,
    agg1,
    agg2,
    agg3,
    agg4,
    agg5,
    agg6,
    agg7
from (
    select i_item_id, ca_country, ca_state, ca_county, avg(agg1) as agg1, avg(agg2) as agg2, avg(agg3) as agg3, avg(agg4) as agg4, avg(agg5) as agg5, avg(agg6) as agg6, avg(agg7) as agg7
    from results
    group by i_item_id, ca_country, ca_state, ca_county
    union all
    select i_item_id, ca_country, ca_state, null as ca_county, avg(agg1), avg(agg2), avg(agg3), avg(agg4), avg(agg5), avg(agg6), avg(agg7)
    from results
    group by i_item_id, ca_country, ca_state
    union all
    select i_item_id, ca_country, null as ca_state, null as ca_county, avg(agg1), avg(agg2), avg(agg3), avg(agg4), avg(agg5), avg(agg6), avg(agg7)
    from results
    group by i_item_id, ca_country
    union all
    select i_item_id, null as ca_country, null as ca_state, null as ca_county, avg(agg1), avg(agg2), avg(agg3), avg(agg4), avg(agg5), avg(agg6), avg(agg7)
    from results
    group by i_item_id
    union all
    select null as i_item_id, null as ca_country, null as ca_state, null as ca_county, avg(agg1), avg(agg2), avg(agg3), avg(agg4), avg(agg5), avg(agg6), avg(agg7)
    from results
) foo
order by ca_country, ca_state, ca_county, i_item_id
limit 100;
