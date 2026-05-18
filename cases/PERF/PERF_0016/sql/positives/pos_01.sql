-- PERF_0016 positive rewrite candidate.
-- Strategy: make joins explicit inside the profit derived table.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

select
    profit.nation,
    profit.o_year,
    sum(profit.amount) as sum_profit
from (
    select
        nation.n_name as nation,
        extract(year from orders.o_orderdate) as o_year,
        lineitem.l_extendedprice * (1 - lineitem.l_discount) - partsupp.ps_supplycost * lineitem.l_quantity as amount
    from part
    join lineitem
      on part.p_partkey = lineitem.l_partkey
    join partsupp
      on partsupp.ps_partkey = lineitem.l_partkey
     and partsupp.ps_suppkey = lineitem.l_suppkey
    join supplier
      on supplier.s_suppkey = lineitem.l_suppkey
    join orders
      on orders.o_orderkey = lineitem.l_orderkey
    join nation
      on supplier.s_nationkey = nation.n_nationkey
    where
        part.p_name like '%turquoise%'
) profit
group by
    profit.nation,
    profit.o_year
order by
    profit.nation,
    profit.o_year desc;
