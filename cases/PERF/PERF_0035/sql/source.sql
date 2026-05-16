-- PERF_0035 source SQL.
-- Frozen from TPC-DS query57.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization only replaces TOP 100 with LIMIT 100.

with v1 as (
    select
        i.i_category,
        i.i_brand,
        cc.cc_name,
        d.d_year,
        d.d_moy,
        sum(cs.cs_sales_price) as sum_sales,
        avg(sum(cs.cs_sales_price)) over (
            partition by i.i_category, i.i_brand, cc.cc_name, d.d_year
        ) as avg_monthly_sales,
        rank() over (
            partition by i.i_category, i.i_brand, cc.cc_name
            order by d.d_year, d.d_moy
        ) as rn
    from item i,
         catalog_sales cs,
         date_dim d,
         call_center cc
    where cs.cs_item_sk = i.i_item_sk
      and cs.cs_sold_date_sk = d.d_date_sk
      and cc.cc_call_center_sk = cs.cs_call_center_sk
      and (
          d.d_year = 2000
          or (d.d_year = 2000 - 1 and d.d_moy = 12)
          or (d.d_year = 2000 + 1 and d.d_moy = 1)
      )
    group by i.i_category, i.i_brand, cc.cc_name, d.d_year, d.d_moy
),
v2 as (
    select
        v1.cc_name,
        v1.d_year,
        v1.d_moy,
        v1.avg_monthly_sales,
        v1.sum_sales,
        v1_lag.sum_sales as psum,
        v1_lead.sum_sales as nsum
    from v1,
         v1 v1_lag,
         v1 v1_lead
    where v1.i_category = v1_lag.i_category
      and v1.i_category = v1_lead.i_category
      and v1.i_brand = v1_lag.i_brand
      and v1.i_brand = v1_lead.i_brand
      and v1.cc_name = v1_lag.cc_name
      and v1.cc_name = v1_lead.cc_name
      and v1.rn = v1_lag.rn + 1
      and v1.rn = v1_lead.rn - 1
)
select *
from v2
where d_year = 2000
  and avg_monthly_sales > 0
  and case
          when avg_monthly_sales > 0
            then abs(sum_sales - avg_monthly_sales) / avg_monthly_sales
          else null
      end > 0.1
order by sum_sales - avg_monthly_sales, nsum
limit 100;
