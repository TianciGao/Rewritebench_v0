-- PERF_0033 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the source manager
-- predicate.

with target_dates as (
    select d_date_sk
    from date_dim
    where d_moy = 12
      and d_year = 2001
),
manager_items as (
    select
        i_item_sk,
        i_brand_id,
        i_brand
    from item
    where i_manager_id = 37
)
select
    mi.i_brand_id as brand_id,
    mi.i_brand as brand,
    sum(ss.ss_ext_sales_price) as ext_price
from target_dates td
join store_sales ss
  on td.d_date_sk = ss.ss_sold_date_sk
join manager_items mi
  on ss.ss_item_sk = mi.i_item_sk
group by mi.i_brand, mi.i_brand_id
order by ext_price desc, mi.i_brand_id
limit 100;
