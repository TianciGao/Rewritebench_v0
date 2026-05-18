-- PERF_0064 positive rewrite SQL.
-- Explicit-join form of the frozen query16 instance.

select count(distinct cs1.cs_order_number) as "order count",
       sum(cs1.cs_ext_ship_cost) as "total shipping cost",
       sum(cs1.cs_net_profit) as "total net profit"
from catalog_sales cs1
join date_dim on cs1.cs_ship_date_sk = d_date_sk
join customer_address on cs1.cs_ship_addr_sk = ca_address_sk
join call_center on cs1.cs_call_center_sk = cc_call_center_sk
where d_date between date '1999-02-01' and (date '1999-02-01' + interval '60 days')
  and ca_state = 'IL'
  and cc_county in ('Williamson County', 'Williamson County', 'Williamson County', 'Williamson County',
                    'Williamson County')
  and exists (
      select 1
      from catalog_sales cs2
      where cs1.cs_order_number = cs2.cs_order_number
        and cs1.cs_warehouse_sk <> cs2.cs_warehouse_sk
  )
  and not exists (
      select 1
      from catalog_returns cr1
      where cs1.cs_order_number = cr1.cr_order_number
  )
order by count(distinct cs1.cs_order_number)
limit 100;
