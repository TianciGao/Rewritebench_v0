-- PERF_0034 positive rewrite candidate.
-- Strategy: factor the shared item/date/address filters and aggregate the three
-- sales channels before unioning them.

with selected_items as (
    select
        i_item_sk,
        i_item_id
    from item
    where i_color in ('orchid', 'chiffon', 'lace')
),
selected_dates as (
    select d_date_sk
    from date_dim
    where d_year = 2000
      and d_moy = 1
),
selected_addresses as (
    select ca_address_sk
    from customer_address
    where ca_gmt_offset = -8
),
channel_sales as (
    select
        si.i_item_id,
        sum(ss.ss_ext_sales_price) as total_sales
    from store_sales ss
    join selected_items si
      on ss.ss_item_sk = si.i_item_sk
    join selected_dates sd
      on ss.ss_sold_date_sk = sd.d_date_sk
    join selected_addresses sa
      on ss.ss_addr_sk = sa.ca_address_sk
    group by si.i_item_id
    union all
    select
        si.i_item_id,
        sum(cs.cs_ext_sales_price) as total_sales
    from catalog_sales cs
    join selected_items si
      on cs.cs_item_sk = si.i_item_sk
    join selected_dates sd
      on cs.cs_sold_date_sk = sd.d_date_sk
    join selected_addresses sa
      on cs.cs_bill_addr_sk = sa.ca_address_sk
    group by si.i_item_id
    union all
    select
        si.i_item_id,
        sum(ws.ws_ext_sales_price) as total_sales
    from web_sales ws
    join selected_items si
      on ws.ws_item_sk = si.i_item_sk
    join selected_dates sd
      on ws.ws_sold_date_sk = sd.d_date_sk
    join selected_addresses sa
      on ws.ws_bill_addr_sk = sa.ca_address_sk
    group by si.i_item_id
)
select
    i_item_id,
    sum(total_sales) as total_sales
from channel_sales
group by i_item_id
order by total_sales, i_item_id
limit 100;
