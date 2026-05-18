-- PERF_0042 negative rewrite.
-- Incorrectly drops item-level and grand rollup rows.
-- Frozen from TPC-DS query_variants/query27a.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization replaces TOP 100 with LIMIT 100 and keeps the generated query shape.

with results as (
    select
        i_item_id,
        s_state,
        0 as g_state,
        ss_quantity as agg1,
        ss_list_price as agg2,
        ss_coupon_amt as agg3,
        ss_sales_price as agg4
    from store_sales, customer_demographics, date_dim, store, item
    where ss_sold_date_sk = d_date_sk
      and ss_item_sk = i_item_sk
      and ss_store_sk = s_store_sk
      and ss_cdemo_sk = cd_demo_sk
      and cd_gender = 'F'
      and cd_marital_status = 'W'
      and cd_education_status = 'Primary'
      and d_year = 1998
      and s_state in ('TN','TN','TN','TN','TN','TN')
)
select
    i_item_id,
    s_state,
    g_state,
    agg1,
    agg2,
    agg3,
    agg4
from (
    select i_item_id, s_state, 0 as g_state,
           avg(agg1) as agg1, avg(agg2) as agg2, avg(agg3) as agg3, avg(agg4) as agg4
    from results
    group by i_item_id, s_state
    union all
    select i_item_id, null as s_state, 1 as g_state,
           avg(agg1) as agg1, avg(agg2) as agg2, avg(agg3) as agg3, avg(agg4) as agg4
    from results
    group by i_item_id
    union all
    select null as i_item_id, null as s_state, 1 as g_state,
           avg(agg1) as agg1, avg(agg2) as agg2, avg(agg3) as agg3, avg(agg4) as agg4
    from results
) foo
where g_state = 0
order by i_item_id, s_state
limit 100;
