-- PERF_0036 source SQL.
-- Frozen from TPC-DS query58.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- PostgreSQL normalization only replaces TOP 100 with LIMIT 100.

with ss_items as (
    select
        i.i_item_id as item_id,
        sum(ss.ss_ext_sales_price) as ss_item_rev
    from store_sales ss,
         item i,
         date_dim d
    where ss.ss_item_sk = i.i_item_sk
      and d.d_date in (
          select d_date
          from date_dim
          where d_week_seq = (
              select d_week_seq
              from date_dim
              where d_date = date '1998-02-19'
          )
      )
      and ss.ss_sold_date_sk = d.d_date_sk
    group by i.i_item_id
),
cs_items as (
    select
        i.i_item_id as item_id,
        sum(cs.cs_ext_sales_price) as cs_item_rev
    from catalog_sales cs,
         item i,
         date_dim d
    where cs.cs_item_sk = i.i_item_sk
      and d.d_date in (
          select d_date
          from date_dim
          where d_week_seq = (
              select d_week_seq
              from date_dim
              where d_date = date '1998-02-19'
          )
      )
      and cs.cs_sold_date_sk = d.d_date_sk
    group by i.i_item_id
),
ws_items as (
    select
        i.i_item_id as item_id,
        sum(ws.ws_ext_sales_price) as ws_item_rev
    from web_sales ws,
         item i,
         date_dim d
    where ws.ws_item_sk = i.i_item_sk
      and d.d_date in (
          select d_date
          from date_dim
          where d_week_seq = (
              select d_week_seq
              from date_dim
              where d_date = date '1998-02-19'
          )
      )
      and ws.ws_sold_date_sk = d.d_date_sk
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
from ss_items,
     cs_items,
     ws_items
where ss_items.item_id = cs_items.item_id
  and ss_items.item_id = ws_items.item_id
  and ss_item_rev between 0.9 * cs_item_rev and 1.1 * cs_item_rev
  and ss_item_rev between 0.9 * ws_item_rev and 1.1 * ws_item_rev
  and cs_item_rev between 0.9 * ss_item_rev and 1.1 * ss_item_rev
  and cs_item_rev between 0.9 * ws_item_rev and 1.1 * ws_item_rev
  and ws_item_rev between 0.9 * ss_item_rev and 1.1 * ss_item_rev
  and ws_item_rev between 0.9 * cs_item_rev and 1.1 * cs_item_rev
order by item_id, ss_item_rev
limit 100;
