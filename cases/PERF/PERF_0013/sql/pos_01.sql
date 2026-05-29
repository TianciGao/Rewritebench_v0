-- PERF_0013 positive rewrite candidate.
-- Strategy: make joins explicit and keep the source region/date filters unchanged.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

select
    nation.n_name,
    sum(lineitem.l_extendedprice * (1 - lineitem.l_discount)) as revenue
from region
join nation
  on region.r_regionkey = nation.n_regionkey
join supplier
  on nation.n_nationkey = supplier.s_nationkey
join lineitem
  on supplier.s_suppkey = lineitem.l_suppkey
join orders
  on lineitem.l_orderkey = orders.o_orderkey
join customer
  on orders.o_custkey = customer.c_custkey
 and supplier.s_nationkey = customer.c_nationkey
where
    region.r_name = 'MIDDLE EAST'
    and orders.o_orderdate >= date '1997-01-01'
    and orders.o_orderdate < date '1997-01-01' + interval '1' year
group by
    nation.n_name
order by
    revenue desc;
