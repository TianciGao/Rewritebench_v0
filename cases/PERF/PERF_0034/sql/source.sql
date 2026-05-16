-- PERF_0034 source SQL.
-- Frozen from TPC-DS query56.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization only replaces TOP 100 with LIMIT 100.

with ss as (
    select
        i.i_item_id,
        sum(ss.ss_ext_sales_price) as total_sales
    from store_sales ss,
         date_dim d,
         customer_address ca,
         item i
    where i.i_item_id in (
        select i_item_id
        from item
        where i_color in ('orchid', 'chiffon', 'lace')
    )
      and ss.ss_item_sk = i.i_item_sk
      and ss.ss_sold_date_sk = d.d_date_sk
      and d.d_year = 2000
      and d.d_moy = 1
      and ss.ss_addr_sk = ca.ca_address_sk
      and ca.ca_gmt_offset = -8
    group by i.i_item_id
),
cs as (
    select
        i.i_item_id,
        sum(cs.cs_ext_sales_price) as total_sales
    from catalog_sales cs,
         date_dim d,
         customer_address ca,
         item i
    where i.i_item_id in (
        select i_item_id
        from item
        where i_color in ('orchid', 'chiffon', 'lace')
    )
      and cs.cs_item_sk = i.i_item_sk
      and cs.cs_sold_date_sk = d.d_date_sk
      and d.d_year = 2000
      and d.d_moy = 1
      and cs.cs_bill_addr_sk = ca.ca_address_sk
      and ca.ca_gmt_offset = -8
    group by i.i_item_id
),
ws as (
    select
        i.i_item_id,
        sum(ws.ws_ext_sales_price) as total_sales
    from web_sales ws,
         date_dim d,
         customer_address ca,
         item i
    where i.i_item_id in (
        select i_item_id
        from item
        where i_color in ('orchid', 'chiffon', 'lace')
    )
      and ws.ws_item_sk = i.i_item_sk
      and ws.ws_sold_date_sk = d.d_date_sk
      and d.d_year = 2000
      and d.d_moy = 1
      and ws.ws_bill_addr_sk = ca.ca_address_sk
      and ca.ca_gmt_offset = -8
    group by i.i_item_id
)
select
    i_item_id,
    sum(total_sales) as total_sales
from (
    select * from ss
    union all
    select * from cs
    union all
    select * from ws
) tmp1
group by i_item_id
order by total_sales, i_item_id
limit 100;
