-- PERF_0032 source SQL.
-- Frozen from TPC-DS query54.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization only replaces TOP 100 with LIMIT 100.

with my_customers as (
    select distinct
        c.c_customer_sk,
        c.c_current_addr_sk
    from (
        select
            cs_sold_date_sk as sold_date_sk,
            cs_bill_customer_sk as customer_sk,
            cs_item_sk as item_sk
        from catalog_sales
        union all
        select
            ws_sold_date_sk as sold_date_sk,
            ws_bill_customer_sk as customer_sk,
            ws_item_sk as item_sk
        from web_sales
    ) cs_or_ws_sales
    join item i
      on cs_or_ws_sales.item_sk = i.i_item_sk
    join date_dim d
      on cs_or_ws_sales.sold_date_sk = d.d_date_sk
    join customer c
      on c.c_customer_sk = cs_or_ws_sales.customer_sk
    where i.i_category = 'Jewelry'
      and i.i_class = 'consignment'
      and d.d_moy = 3
      and d.d_year = 1999
),
my_revenue as (
    select
        mc.c_customer_sk,
        sum(ss.ss_ext_sales_price) as revenue
    from my_customers mc
    join customer_address ca
      on mc.c_current_addr_sk = ca.ca_address_sk
    join store s
      on ca.ca_county = s.s_county
     and ca.ca_state = s.s_state
    join store_sales ss
      on mc.c_customer_sk = ss.ss_customer_sk
    join date_dim d
      on ss.ss_sold_date_sk = d.d_date_sk
    where d.d_month_seq between (
        select distinct d_month_seq + 1
        from date_dim
        where d_year = 1999
          and d_moy = 3
    ) and (
        select distinct d_month_seq + 3
        from date_dim
        where d_year = 1999
          and d_moy = 3
    )
    group by mc.c_customer_sk
),
segments as (
    select cast((revenue / 50) as integer) as segment
    from my_revenue
)
select
    segment,
    count(*) as num_customers,
    segment * 50 as segment_base
from segments
group by segment
order by segment, num_customers
limit 100;
