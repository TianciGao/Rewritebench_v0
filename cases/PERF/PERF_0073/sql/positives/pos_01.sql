with
b1 as (
  select avg(ss_list_price) b1_lp, count(ss_list_price) b1_cnt, count(distinct ss_list_price) b1_cntd
  from store_sales
  where ss_quantity between 0 and 5
    and (ss_list_price between 11 and 21 or ss_coupon_amt between 460 and 1460 or ss_wholesale_cost between 14 and 34)
),
b2 as (
  select avg(ss_list_price) b2_lp, count(ss_list_price) b2_cnt, count(distinct ss_list_price) b2_cntd
  from store_sales
  where ss_quantity between 6 and 10
    and (ss_list_price between 91 and 101 or ss_coupon_amt between 1430 and 2430 or ss_wholesale_cost between 32 and 52)
),
b3 as (
  select avg(ss_list_price) b3_lp, count(ss_list_price) b3_cnt, count(distinct ss_list_price) b3_cntd
  from store_sales
  where ss_quantity between 11 and 15
    and (ss_list_price between 66 and 76 or ss_coupon_amt between 920 and 1920 or ss_wholesale_cost between 4 and 24)
),
b4 as (
  select avg(ss_list_price) b4_lp, count(ss_list_price) b4_cnt, count(distinct ss_list_price) b4_cntd
  from store_sales
  where ss_quantity between 16 and 20
    and (ss_list_price between 142 and 152 or ss_coupon_amt between 3054 and 4054 or ss_wholesale_cost between 80 and 100)
),
b5 as (
  select avg(ss_list_price) b5_lp, count(ss_list_price) b5_cnt, count(distinct ss_list_price) b5_cntd
  from store_sales
  where ss_quantity between 21 and 25
    and (ss_list_price between 135 and 145 or ss_coupon_amt between 14180 and 15180 or ss_wholesale_cost between 38 and 58)
),
b6 as (
  select avg(ss_list_price) b6_lp, count(ss_list_price) b6_cnt, count(distinct ss_list_price) b6_cntd
  from store_sales
  where ss_quantity between 26 and 30
    and (ss_list_price between 28 and 38 or ss_coupon_amt between 2513 and 3513 or ss_wholesale_cost between 42 and 62)
)
select *
from b1 cross join b2 cross join b3 cross join b4 cross join b5 cross join b6
limit 100;
