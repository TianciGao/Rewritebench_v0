-- PERF_0022 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the large-volume threshold.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    customer.c_name,
    customer.c_custkey,
    orders.o_orderkey,
    orders.o_orderdate,
    orders.o_totalprice,
    sum(lineitem.l_quantity)
from customer
join orders
  on customer.c_custkey = orders.o_custkey
join lineitem
  on orders.o_orderkey = lineitem.l_orderkey
join (
    select
        l_orderkey
    from lineitem
    group by
        l_orderkey
    having
        sum(l_quantity) > 300
) large_orders
  on large_orders.l_orderkey = orders.o_orderkey
group by
    customer.c_name,
    customer.c_custkey,
    orders.o_orderkey,
    orders.o_orderdate,
    orders.o_totalprice
order by
    orders.o_totalprice desc,
    orders.o_orderdate
limit 100;
