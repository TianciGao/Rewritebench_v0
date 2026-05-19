-- PERF_0008 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the customer segment predicate.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    lineitem.l_orderkey,
    sum(lineitem.l_extendedprice * (1 - lineitem.l_discount)) as revenue,
    orders_filtered.o_orderdate,
    orders_filtered.o_shippriority
from (
    select
        c_custkey
    from customer
    where c_mktsegment = 'BUILDING'
) customer_filtered
join (
    select
        o_orderkey,
        o_custkey,
        o_orderdate,
        o_shippriority
    from orders
    where o_orderdate < date '1995-03-27'
) orders_filtered
  on customer_filtered.c_custkey = orders_filtered.o_custkey
join lineitem
  on orders_filtered.o_orderkey = lineitem.l_orderkey
where
    lineitem.l_shipdate > date '1995-03-27'
group by
    lineitem.l_orderkey,
    orders_filtered.o_orderdate,
    orders_filtered.o_shippriority
order by
    revenue desc,
    orders_filtered.o_orderdate
limit 10;
