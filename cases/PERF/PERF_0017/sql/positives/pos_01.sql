-- PERF_0017 positive rewrite candidate.
-- Strategy: make joins explicit while preserving the date window and return-flag filter.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

select
    customer.c_custkey,
    customer.c_name,
    sum(lineitem.l_extendedprice * (1 - lineitem.l_discount)) as revenue,
    customer.c_acctbal,
    nation.n_name,
    customer.c_address,
    customer.c_phone,
    customer.c_comment
from customer
join orders
  on customer.c_custkey = orders.o_custkey
join lineitem
  on lineitem.l_orderkey = orders.o_orderkey
join nation
  on customer.c_nationkey = nation.n_nationkey
where
    orders.o_orderdate >= date '1993-11-01'
    and orders.o_orderdate < date '1993-11-01' + interval '3' month
    and lineitem.l_returnflag = 'R'
group by
    customer.c_custkey,
    customer.c_name,
    customer.c_acctbal,
    customer.c_phone,
    nation.n_name,
    customer.c_address,
    customer.c_comment
order by
    revenue desc
limit 20;
