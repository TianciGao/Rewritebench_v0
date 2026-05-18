-- PERF_0036 positive rewrite candidate.
-- Strategy: factor the target week and aggregate each sales channel explicitly.

with target_week_dates as (
    select d_date_sk
    from date_dim
    where d_week_seq = (
        select d_week_seq
        from date_dim
        where d_date = date '1998-02-19'
    )
),
ss_items as (
    select
        i.i_item_id as item_id,
        sum(ss.ss_ext_sales_price) as ss_item_rev
    from store_sales ss
    join item i
      on ss.ss_item_sk = i.i_item_sk
    join target_week_dates twd
      on ss.ss_sold_date_sk = twd.d_date_sk
    group by i.i_item_id
),
cs_items as (
    select
        i.i_item_id as item_id,
        sum(cs.cs_ext_sales_price) as cs_item_rev
    from catalog_sales cs
    join item i
      on cs.cs_item_sk = i.i_item_sk
    join target_week_dates twd
      on cs.cs_sold_date_sk = twd.d_date_sk
    group by i.i_item_id
),
ws_items as (
    select
        i.i_item_id as item_id,
        sum(ws.ws_ext_sales_price) as ws_item_rev
    from web_sales ws
    join item i
      on ws.ws_item_sk = i.i_item_sk
    join target_week_dates twd
      on ws.ws_sold_date_sk = twd.d_date_sk
    group by i.i_item_id
)
select
    ss_items.item_id,
    ss_item_rev,
    ss_item_rev / ((ss_item_rev + cs_item_rev + ws_item_rev) / 3) * 100 as ss_dev,
    cs_item_rev,
    cs_item_rev / ((ss_item_rev + cs_item_rev + ws_item_rev) / 3) * 100 as cs_dev,
    ws_item_rev,
    ws_item_rev / ((ss_item_rev + cs_item_rev + ws_item_rev) / 3) * 100 as ws_dev,
    (ss_item_rev + cs_item_rev + ws_item_rev) / 3 as average
from ss_items
join cs_items
  on ss_items.item_id = cs_items.item_id
join ws_items
  on ss_items.item_id = ws_items.item_id
where ss_item_rev between 0.9 * cs_item_rev and 1.1 * cs_item_rev
  and ss_item_rev between 0.9 * ws_item_rev and 1.1 * ws_item_rev
  and cs_item_rev between 0.9 * ss_item_rev and 1.1 * ss_item_rev
  and cs_item_rev between 0.9 * ws_item_rev and 1.1 * ws_item_rev
  and ws_item_rev between 0.9 * ss_item_rev and 1.1 * ss_item_rev
  and ws_item_rev between 0.9 * cs_item_rev and 1.1 * cs_item_rev
order by item_id, ss_item_rev
limit 100;
