-- PERF_0054 positive rewrite SQL.
-- Frozen from TPC-DS query_templates/query3.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization replaces TOP 100 with LIMIT 100.

select
    dt.d_year,
    item.i_brand_id brand_id,
    item.i_brand brand,
    sum(ss_ext_sales_price) sum_agg
from date_dim dt
join store_sales on dt.d_date_sk = store_sales.ss_sold_date_sk
join item on store_sales.ss_item_sk = item.i_item_sk
where true
  and item.i_manufact_id = 436
  and dt.d_moy = 12
group by dt.d_year, item.i_brand, item.i_brand_id
order by dt.d_year, sum_agg desc, brand_id
limit 100;
