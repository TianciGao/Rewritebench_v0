with customer_total_return as (
  select
    wr.wr_returning_customer_sk as ctr_customer_sk,
    ca.ca_state as ctr_state,
    sum(wr.wr_return_amt) as ctr_total_return
  from web_returns wr
  join date_dim d on wr.wr_returned_date_sk = d.d_date_sk
  join customer_address ca on wr.wr_returning_addr_sk = ca.ca_address_sk
  where d.d_year = 2002
  group by wr.wr_returning_customer_sk, ca.ca_state
)
select
  c.c_customer_id,
  c.c_salutation,
  c.c_first_name,
  c.c_last_name,
  c.c_preferred_cust_flag,
  c.c_birth_day,
  c.c_birth_month,
  c.c_birth_year,
  c.c_birth_country,
  c.c_login,
  c.c_email_address,
  c.c_last_review_date_sk,
  ctr1.ctr_total_return
from customer_total_return ctr1
join customer c on ctr1.ctr_customer_sk = c.c_customer_sk
join customer_address ca on ca.ca_address_sk = c.c_current_addr_sk
where ctr1.ctr_total_return > (
    select avg(ctr2.ctr_total_return) * 2.0
    from customer_total_return ctr2
    where ctr1.ctr_state = ctr2.ctr_state
  )
  and ca.ca_state = 'IL'
order by
  c.c_customer_id, c.c_salutation, c.c_first_name, c.c_last_name, c.c_preferred_cust_flag,
  c.c_birth_day, c.c_birth_month, c.c_birth_year, c.c_birth_country, c.c_login, c.c_email_address,
  c.c_last_review_date_sk, ctr1.ctr_total_return
limit 100;
