-- PERF_0025 negative rewrite candidate.
-- Strategy: keep the positive rewrite shape but change the target nation from IRAQ to IRAN.
-- Non-equivalence is not yet proven.

select
    supplier.s_name,
    count(*) as numwait
from
    supplier
    join lineitem l1
        on supplier.s_suppkey = l1.l_suppkey
    join orders
        on orders.o_orderkey = l1.l_orderkey
    join nation
        on supplier.s_nationkey = nation.n_nationkey
where
    orders.o_orderstatus = 'F'
    and l1.l_receiptdate > l1.l_commitdate
    and exists (
        select
            1
        from
            lineitem l2
        where
            l2.l_orderkey = l1.l_orderkey
            and l2.l_suppkey <> l1.l_suppkey
    )
    and not exists (
        select
            1
        from
            lineitem l3
        where
            l3.l_orderkey = l1.l_orderkey
            and l3.l_suppkey <> l1.l_suppkey
            and l3.l_receiptdate > l3.l_commitdate
    )
    and nation.n_name = 'IRAN'
group by
    supplier.s_name
order by
    numwait desc,
    supplier.s_name
limit 100;
