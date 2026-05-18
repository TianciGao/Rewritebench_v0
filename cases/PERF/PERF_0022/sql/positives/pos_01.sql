-- PERF_0022 positive rewrite candidate.
-- Strategy: make joins explicit and precompute large-volume order keys.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

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
        sum(l_quantity) > 312
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
