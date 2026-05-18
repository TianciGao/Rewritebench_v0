-- PERF_0014 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but drop the opposite-direction nation pair.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    shipping.supp_nation,
    shipping.cust_nation,
    shipping.l_year,
    sum(shipping.volume) as revenue
from (
    select
        supplier_nation.n_name as supp_nation,
        customer_nation.n_name as cust_nation,
        extract(year from lineitem.l_shipdate) as l_year,
        lineitem.l_extendedprice * (1 - lineitem.l_discount) as volume
    from supplier
    join lineitem
      on supplier.s_suppkey = lineitem.l_suppkey
    join orders
      on lineitem.l_orderkey = orders.o_orderkey
    join customer
      on orders.o_custkey = customer.c_custkey
    join nation supplier_nation
      on supplier.s_nationkey = supplier_nation.n_nationkey
    join nation customer_nation
      on customer.c_nationkey = customer_nation.n_nationkey
    where
        (
            (supplier_nation.n_name = 'BRAZIL' and customer_nation.n_name = 'MOROCCO')
            or (supplier_nation.n_name = 'BRAZIL' and customer_nation.n_name = 'MOROCCO')
        )
        and lineitem.l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by
    shipping.supp_nation,
    shipping.cust_nation,
    shipping.l_year
order by
    shipping.supp_nation,
    shipping.cust_nation,
    shipping.l_year;
