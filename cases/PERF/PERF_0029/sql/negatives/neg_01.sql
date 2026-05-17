-- PERF_0029 negative rewrite candidate.
-- Strategy: invert the comment filter so only matching orders are counted.

select
    ordercount,
    count(*) as custdist
from (
    select
        customer.c_custkey,
        count(orders.o_orderkey) as ordercount
    from customer
    left join orders
      on customer.c_custkey = orders.o_custkey
     and orders.o_comment like '%express%deposits%'
    group by
        customer.c_custkey
) orders_per_cust
group by
    ordercount
order by
    custdist desc,
    ordercount desc;
