-- PERF_0032 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the source category filter.

with seed_sales as (
    select
        cs_sold_date_sk as sold_date_sk,
        cs_bill_customer_sk as customer_sk,
        cs_item_sk as item_sk
    from catalog_sales
    union all
    select
        ws_sold_date_sk,
        ws_bill_customer_sk,
        ws_item_sk
    from web_sales
),
march_1999_customers as (
    select distinct
        c.c_customer_sk,
        c.c_current_addr_sk
    from seed_sales ss
    join item i
      on ss.item_sk = i.i_item_sk
    join date_dim d
      on ss.sold_date_sk = d.d_date_sk
    join customer c
      on ss.customer_sk = c.c_customer_sk
    where i.i_category = 'Music'
      and i.i_class = 'consignment'
      and d.d_moy = 3
      and d.d_year = 1999
),
target_months as (
    select d_month_seq
    from date_dim
    where d_month_seq between (
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
),
customer_revenue as (
    select
        mc.c_customer_sk,
        sum(ss.ss_ext_sales_price) as revenue
    from march_1999_customers mc
    join customer_address ca
      on mc.c_current_addr_sk = ca.ca_address_sk
    join store s
      on ca.ca_county = s.s_county
     and ca.ca_state = s.s_state
    join store_sales ss
      on mc.c_customer_sk = ss.ss_customer_sk
    join date_dim d
      on ss.ss_sold_date_sk = d.d_date_sk
    join target_months tm
      on d.d_month_seq = tm.d_month_seq
    group by mc.c_customer_sk
)
select
    cast((revenue / 50) as integer) as segment,
    count(*) as num_customers,
    cast((revenue / 50) as integer) * 50 as segment_base
from customer_revenue
group by cast((revenue / 50) as integer)
order by segment, num_customers
limit 100;
