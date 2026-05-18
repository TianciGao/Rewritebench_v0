-- PERF_0041 source SQL.
-- Frozen from TPC-DS query_variants/query22a.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization replaces TOP 100 with LIMIT 100.

with results as (
    select
        i.i_product_name,
        i.i_brand,
        i.i_class,
        i.i_category,
        inv.inv_quantity_on_hand as qoh
    from inventory inv,
         date_dim d,
         item i,
         warehouse w
    where inv.inv_date_sk = d.d_date_sk
      and inv.inv_item_sk = i.i_item_sk
      and inv.inv_warehouse_sk = w.w_warehouse_sk
      and d.d_month_seq between 1212 and 1212 + 11
),
results_rollup as (
    select i_product_name, i_brand, i_class, i_category, avg(qoh) as qoh
    from results
    group by i_product_name, i_brand, i_class, i_category
    union all
    select i_product_name, i_brand, i_class, null as i_category, avg(qoh)
    from results
    group by i_product_name, i_brand, i_class
    union all
    select i_product_name, i_brand, null as i_class, null as i_category, avg(qoh)
    from results
    group by i_product_name, i_brand
    union all
    select i_product_name, null as i_brand, null as i_class, null as i_category, avg(qoh)
    from results
    group by i_product_name
    union all
    select null as i_product_name, null as i_brand, null as i_class, null as i_category, avg(qoh)
    from results
)
select
    i_product_name,
    i_brand,
    i_class,
    i_category,
    qoh
from results_rollup
order by qoh, i_product_name, i_brand, i_class, i_category
limit 100;
