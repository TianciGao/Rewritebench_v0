-- PERF_0066 positive rewrite SQL.
-- Explicit-join form of the frozen query19 instance.

select i_brand_id as brand_id,
       i_brand as brand,
       i_manufact_id,
       i_manufact,
       sum(ss_ext_sales_price) as ext_price
from store_sales
join date_dim on d_date_sk = ss_sold_date_sk
join item on ss_item_sk = i_item_sk
join customer on ss_customer_sk = c_customer_sk
join customer_address on c_current_addr_sk = ca_address_sk
join store on ss_store_sk = s_store_sk
where i_manager_id = 7
  and d_moy = 11
  and d_year = 1999
  and substr(ca_zip, 1, 5) <> substr(s_zip, 1, 5)
group by i_brand,
         i_brand_id,
         i_manufact_id,
         i_manufact
order by ext_price desc,
         i_brand,
         i_brand_id,
         i_manufact_id,
         i_manufact
limit 100;
