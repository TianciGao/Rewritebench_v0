select
  i.i_item_id,
  avg(cs.cs_quantity) agg1,
  avg(cs.cs_list_price) agg2,
  avg(cs.cs_coupon_amt) agg3,
  avg(cs.cs_sales_price) agg4
from catalog_sales cs
join customer_demographics cd on cs.cs_bill_cdemo_sk = cd.cd_demo_sk
join date_dim d on cs.cs_sold_date_sk = d.d_date_sk
join item i on cs.cs_item_sk = i.i_item_sk
join promotion p on cs.cs_promo_sk = p.p_promo_sk
where cd.cd_gender = 'F'
  and cd.cd_marital_status = 'W'
  and cd.cd_education_status = 'Primary'
  and p.p_channel_email = 'Y'
  and p.p_channel_event = 'Y'
  and d.d_year = 1998
group by i.i_item_id
order by i.i_item_id
limit 100;
