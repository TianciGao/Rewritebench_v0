-- PERF_0041 negative rewrite.
-- Incorrectly shifts the inventory month range away from the frozen dsqgen range.

with results as (
    select
        i.i_product_name,
        i.i_brand,
        i.i_class,
        i.i_category,
        inv.inv_quantity_on_hand as qoh
    from inventory inv,
         date_dim d,
         item i,
         warehouse w
    where inv.inv_date_sk = d.d_date_sk
      and inv.inv_item_sk = i.i_item_sk
      and inv.inv_warehouse_sk = w.w_warehouse_sk
      and d.d_month_seq between 9999 and 9999 + 11
)
select
    i_product_name,
    i_brand,
    i_class,
    i_category,
    avg(qoh) as qoh
from results
group by i_product_name, i_brand, i_class, i_category
order by qoh, i_product_name, i_brand, i_class, i_category
limit 100;
