with ss as (
  select ca.ca_county, d.d_qoy, d.d_year, sum(ss.ss_ext_sales_price) as store_sales
  from store_sales ss
  join date_dim d on ss.ss_sold_date_sk = d.d_date_sk
  join customer_address ca on ss.ss_addr_sk = ca.ca_address_sk
  group by ca.ca_county, d.d_qoy, d.d_year
),
ws as (
  select ca.ca_county, d.d_qoy, d.d_year, sum(ws.ws_ext_sales_price) as web_sales
  from web_sales ws
  join date_dim d on ws.ws_sold_date_sk = d.d_date_sk
  join customer_address ca on ws.ws_bill_addr_sk = ca.ca_address_sk
  group by ca.ca_county, d.d_qoy, d.d_year
)
select
  ss1.ca_county,
  ss1.d_year,
  ws2.web_sales / ws1.web_sales as web_q1_q2_increase,
  ss2.store_sales / ss1.store_sales as store_q1_q2_increase,
  ws3.web_sales / ws2.web_sales as web_q2_q3_increase,
  ss3.store_sales / ss2.store_sales as store_q2_q3_increase
from ss ss1
join ss ss2 on ss1.ca_county = ss2.ca_county
join ss ss3 on ss2.ca_county = ss3.ca_county
join ws ws1 on ss1.ca_county = ws1.ca_county
join ws ws2 on ws1.ca_county = ws2.ca_county
join ws ws3 on ws1.ca_county = ws3.ca_county
where ss1.d_qoy = 1
  and ss1.d_year = 2000
  and ss2.d_qoy = 2
  and ss2.d_year = 2000
  and ss3.d_qoy = 3
  and ss3.d_year = 2000
  and ws1.d_qoy = 1
  and ws1.d_year = 2000
  and ws2.d_qoy = 2
  and ws2.d_year = 2000
  and ws3.d_qoy = 3
  and ws3.d_year = 2000
  and case when ws1.web_sales > 0 then ws2.web_sales / ws1.web_sales else null end
    > case when ss1.store_sales > 0 then ss2.store_sales / ss1.store_sales else null end
  and case when ws2.web_sales > 0 then ws3.web_sales / ws2.web_sales else null end
    > case when ss2.store_sales > 0 then ss3.store_sales / ss2.store_sales else null end
order by ss1.d_year;
