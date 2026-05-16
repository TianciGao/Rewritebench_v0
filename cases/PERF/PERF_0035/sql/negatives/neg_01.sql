-- PERF_0035 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the final year filter.

with base_sales as (
    select
        i.i_category,
        i.i_brand,
        cc.cc_name,
        d.d_year,
        d.d_moy,
        cs.cs_sales_price
    from catalog_sales cs
    join item i
      on cs.cs_item_sk = i.i_item_sk
    join date_dim d
      on cs.cs_sold_date_sk = d.d_date_sk
    join call_center cc
      on cs.cs_call_center_sk = cc.cc_call_center_sk
    where d.d_year = 2000
       or (d.d_year = 1999 and d.d_moy = 12)
       or (d.d_year = 2001 and d.d_moy = 1)
),
v1 as (
    select
        i_category,
        i_brand,
        cc_name,
        d_year,
        d_moy,
        sum(cs_sales_price) as sum_sales,
        avg(sum(cs_sales_price)) over (
            partition by i_category, i_brand, cc_name, d_year
        ) as avg_monthly_sales,
        rank() over (
            partition by i_category, i_brand, cc_name
            order by d_year, d_moy
        ) as rn
    from base_sales
    group by i_category, i_brand, cc_name, d_year, d_moy
),
v2 as (
    select
        cur.cc_name,
        cur.d_year,
        cur.d_moy,
        cur.avg_monthly_sales,
        cur.sum_sales,
        prev.sum_sales as psum,
        next_row.sum_sales as nsum
    from v1 cur
    join v1 prev
      on cur.i_category = prev.i_category
     and cur.i_brand = prev.i_brand
     and cur.cc_name = prev.cc_name
     and cur.rn = prev.rn + 1
    join v1 next_row
      on cur.i_category = next_row.i_category
     and cur.i_brand = next_row.i_brand
     and cur.cc_name = next_row.cc_name
     and cur.rn = next_row.rn - 1
)
select *
from v2
where d_year = 1999
  and avg_monthly_sales > 0
  and abs(sum_sales - avg_monthly_sales) / avg_monthly_sales > 0.1
order by sum_sales - avg_monthly_sales, nsum
limit 100;
