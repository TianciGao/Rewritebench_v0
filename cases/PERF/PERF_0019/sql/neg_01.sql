-- PERF_0019 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the excluded comment phrase.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    customer_order_counts.c_count,
    count(*) as custdist
from (
    select
        customer.c_custkey,
        count(orders.o_orderkey) as c_count
    from customer
    left join orders
      on customer.c_custkey = orders.o_custkey
     and orders.o_comment not like '%special%deposits%'
    group by
        customer.c_custkey
) customer_order_counts
group by
    customer_order_counts.c_count
order by
    custdist desc,
    customer_order_counts.c_count desc;
