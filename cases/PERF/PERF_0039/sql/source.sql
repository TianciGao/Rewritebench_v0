-- PERF_0039 source SQL.
-- Frozen from TPC-DS query_variants/query14a.tpl via repaired repo-local dsqgen:
--   COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi
-- query14a emits two SELECT statements; both are preserved here with PostgreSQL LIMIT syntax.

with cross_items as (
    select i.i_item_sk as ss_item_sk
    from item i,
         (
             select iss.i_brand_id as brand_id, iss.i_class_id as class_id, iss.i_category_id as category_id
             from store_sales ss, item iss, date_dim d1
             where ss.ss_item_sk = iss.i_item_sk
               and ss.ss_sold_date_sk = d1.d_date_sk
               and d1.d_year between 1999 and 1999 + 2
             intersect
             select ics.i_brand_id, ics.i_class_id, ics.i_category_id
             from catalog_sales cs, item ics, date_dim d2
             where cs.cs_item_sk = ics.i_item_sk
               and cs.cs_sold_date_sk = d2.d_date_sk
               and d2.d_year between 1999 and 1999 + 2
             intersect
             select iws.i_brand_id, iws.i_class_id, iws.i_category_id
             from web_sales ws, item iws, date_dim d3
             where ws.ws_item_sk = iws.i_item_sk
               and ws.ws_sold_date_sk = d3.d_date_sk
               and d3.d_year between 1999 and 1999 + 2
         ) x
    where i.i_brand_id = x.brand_id
      and i.i_class_id = x.class_id
      and i.i_category_id = x.category_id
),
avg_sales as (
    select avg(quantity * list_price) as average_sales
    from (
        select ss_quantity as quantity, ss_list_price as list_price
        from store_sales ss, date_dim d
        where ss.ss_sold_date_sk = d.d_date_sk
          and d.d_year between 1999 and 2001
        union all
        select cs_quantity, cs_list_price
        from catalog_sales cs, date_dim d
        where cs.cs_sold_date_sk = d.d_date_sk
          and d.d_year between 1998 and 1998 + 2
        union all
        select ws_quantity, ws_list_price
        from web_sales ws, date_dim d
        where ws.ws_sold_date_sk = d.d_date_sk
          and d.d_year between 1998 and 1998 + 2
    ) x
),
results as (
    select channel, i_brand_id, i_class_id, i_category_id, sum(sales) as sum_sales, sum(number_sales) as number_sales
    from (
        select 'store' as channel, i.i_brand_id, i.i_class_id, i.i_category_id, sum(ss.ss_quantity * ss.ss_list_price) as sales, count(*) as number_sales
        from store_sales ss, item i, date_dim d
        where ss.ss_item_sk in (select ss_item_sk from cross_items)
          and ss.ss_item_sk = i.i_item_sk
          and ss.ss_sold_date_sk = d.d_date_sk
          and d.d_year = 1998 + 2
          and d.d_moy = 11
        group by i.i_brand_id, i.i_class_id, i.i_category_id
        having sum(ss.ss_quantity * ss.ss_list_price) > (select average_sales from avg_sales)
        union all
        select 'catalog', i.i_brand_id, i.i_class_id, i.i_category_id, sum(cs.cs_quantity * cs.cs_list_price), count(*)
        from catalog_sales cs, item i, date_dim d
        where cs.cs_item_sk in (select ss_item_sk from cross_items)
          and cs.cs_item_sk = i.i_item_sk
          and cs.cs_sold_date_sk = d.d_date_sk
          and d.d_year = 1998 + 2
          and d.d_moy = 11
        group by i.i_brand_id, i.i_class_id, i.i_category_id
        having sum(cs.cs_quantity * cs.cs_list_price) > (select average_sales from avg_sales)
        union all
        select 'web', i.i_brand_id, i.i_class_id, i.i_category_id, sum(ws.ws_quantity * ws.ws_list_price), count(*)
        from web_sales ws, item i, date_dim d
        where ws.ws_item_sk in (select ss_item_sk from cross_items)
          and ws.ws_item_sk = i.i_item_sk
          and ws.ws_sold_date_sk = d.d_date_sk
          and d.d_year = 1998 + 2
          and d.d_moy = 11
        group by i.i_brand_id, i.i_class_id, i.i_category_id
        having sum(ws.ws_quantity * ws.ws_list_price) > (select average_sales from avg_sales)
    ) y
    group by channel, i_brand_id, i_class_id, i_category_id
)
select channel, i_brand_id, i_class_id, i_category_id, sum_sales, number_sales
from (
    select channel, i_brand_id, i_class_id, i_category_id, sum_sales, number_sales from results
    union
    select channel, i_brand_id, i_class_id, null as i_category_id, sum(sum_sales), sum(number_sales) from results group by channel, i_brand_id, i_class_id
    union
    select channel, i_brand_id, null as i_class_id, null as i_category_id, sum(sum_sales), sum(number_sales) from results group by channel, i_brand_id
    union
    select channel, null as i_brand_id, null as i_class_id, null as i_category_id, sum(sum_sales), sum(number_sales) from results group by channel
    union
    select null as channel, null as i_brand_id, null as i_class_id, null as i_category_id, sum(sum_sales), sum(number_sales) from results
) z
order by channel, i_brand_id, i_class_id, i_category_id
limit 100;

with cross_items as (
    select i.i_item_sk as ss_item_sk
    from item i,
         (
             select iss.i_brand_id as brand_id, iss.i_class_id as class_id, iss.i_category_id as category_id
             from store_sales ss, item iss, date_dim d1
             where ss.ss_item_sk = iss.i_item_sk
               and ss.ss_sold_date_sk = d1.d_date_sk
               and d1.d_year between 1999 and 1999 + 2
             intersect
             select ics.i_brand_id, ics.i_class_id, ics.i_category_id
             from catalog_sales cs, item ics, date_dim d2
             where cs.cs_item_sk = ics.i_item_sk
               and cs.cs_sold_date_sk = d2.d_date_sk
               and d2.d_year between 1999 and 1999 + 2
             intersect
             select iws.i_brand_id, iws.i_class_id, iws.i_category_id
             from web_sales ws, item iws, date_dim d3
             where ws.ws_item_sk = iws.i_item_sk
               and ws.ws_sold_date_sk = d3.d_date_sk
               and d3.d_year between 1999 and 1999 + 2
         ) x
    where i.i_brand_id = x.brand_id
      and i.i_class_id = x.class_id
      and i.i_category_id = x.category_id
),
avg_sales as (
    select avg(quantity * list_price) as average_sales
    from (
        select ss_quantity as quantity, ss_list_price as list_price
        from store_sales ss, date_dim d
        where ss.ss_sold_date_sk = d.d_date_sk
          and d.d_year between 1998 and 1998 + 2
        union all
        select cs_quantity, cs_list_price
        from catalog_sales cs, date_dim d
        where cs.cs_sold_date_sk = d.d_date_sk
          and d.d_year between 1998 and 1998 + 2
        union all
        select ws_quantity, ws_list_price
        from web_sales ws, date_dim d
        where ws.ws_sold_date_sk = d.d_date_sk
          and d.d_year between 1998 and 1998 + 2
    ) x
)
select *
from (
    select 'store' as channel, i.i_brand_id, i.i_class_id, i.i_category_id, sum(ss.ss_quantity * ss.ss_list_price) as sales, count(*) as number_sales
    from store_sales ss, item i, date_dim d
    where ss.ss_item_sk in (select ss_item_sk from cross_items)
      and ss.ss_item_sk = i.i_item_sk
      and ss.ss_sold_date_sk = d.d_date_sk
      and d.d_week_seq = (select d_week_seq from date_dim where d_year = 1998 + 1 and d_moy = 12 and d_dom = 16)
    group by i.i_brand_id, i.i_class_id, i.i_category_id
    having sum(ss.ss_quantity * ss.ss_list_price) > (select average_sales from avg_sales)
) this_year,
(
    select 'store' as channel, i.i_brand_id, i.i_class_id, i.i_category_id, sum(ss.ss_quantity * ss.ss_list_price) as sales, count(*) as number_sales
    from store_sales ss, item i, date_dim d
    where ss.ss_item_sk in (select ss_item_sk from cross_items)
      and ss.ss_item_sk = i.i_item_sk
      and ss.ss_sold_date_sk = d.d_date_sk
      and d.d_week_seq = (select d_week_seq from date_dim where d_year = 1998 and d_moy = 12 and d_dom = 16)
    group by i.i_brand_id, i.i_class_id, i.i_category_id
    having sum(ss.ss_quantity * ss.ss_list_price) > (select average_sales from avg_sales)
) last_year
where this_year.i_brand_id = last_year.i_brand_id
  and this_year.i_class_id = last_year.i_class_id
  and this_year.i_category_id = last_year.i_category_id
order by this_year.channel, this_year.i_brand_id, this_year.i_class_id, this_year.i_category_id
limit 100;
