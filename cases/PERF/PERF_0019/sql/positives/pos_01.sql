-- PERF_0019 positive rewrite candidate.
-- Strategy: make the derived-table aliases explicit while preserving left join predicate placement.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

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
     and orders.o_comment not like '%express%deposits%'
    group by
        customer.c_custkey
) customer_order_counts
group by
    customer_order_counts.c_count
order by
    custdist desc,
    customer_order_counts.c_count desc;
