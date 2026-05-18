-- PERF_0015 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the focus nation in the numerator.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    all_nations.o_year,
    sum(case
        when all_nations.nation = 'IRAQ' then all_nations.volume
        else 0
    end) / sum(all_nations.volume) as mkt_share
from (
    select
        extract(year from orders.o_orderdate) as o_year,
        lineitem.l_extendedprice * (1 - lineitem.l_discount) as volume,
        supplier_nation.n_name as nation
    from part
    join lineitem
      on part.p_partkey = lineitem.l_partkey
    join supplier
      on supplier.s_suppkey = lineitem.l_suppkey
    join orders
      on lineitem.l_orderkey = orders.o_orderkey
    join customer
      on orders.o_custkey = customer.c_custkey
    join nation customer_nation
      on customer.c_nationkey = customer_nation.n_nationkey
    join region
      on customer_nation.n_regionkey = region.r_regionkey
    join nation supplier_nation
      on supplier.s_nationkey = supplier_nation.n_nationkey
    where
        region.r_name = 'MIDDLE EAST'
        and orders.o_orderdate between date '1995-01-01' and date '1996-12-31'
        and part.p_type = 'MEDIUM POLISHED STEEL'
) all_nations
group by
    all_nations.o_year
order by
    all_nations.o_year;
