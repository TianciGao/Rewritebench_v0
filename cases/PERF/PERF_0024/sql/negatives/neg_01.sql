-- PERF_0024 negative rewrite candidate.
-- Strategy: keep the positive rewrite shape but change the part-name prefix from 'pale%' to 'blue%'.
-- Non-equivalence is not yet proven.

select
    supplier.s_name,
    supplier.s_address
from
    supplier
    join nation
        on supplier.s_nationkey = nation.n_nationkey
where
    nation.n_name = 'BRAZIL'
    and exists (
        select
            1
        from
            partsupp
            join part
                on partsupp.ps_partkey = part.p_partkey
        where
            partsupp.ps_suppkey = supplier.s_suppkey
            and part.p_name like 'blue%'
            and partsupp.ps_availqty > (
                select
                    0.5 * sum(lineitem.l_quantity)
                from
                    lineitem
                where
                    lineitem.l_partkey = partsupp.ps_partkey
                    and lineitem.l_suppkey = partsupp.ps_suppkey
                    and lineitem.l_shipdate >= date '1997-01-01'
                    and lineitem.l_shipdate < date '1997-01-01' + interval '1' year
            )
    )
order by
    supplier.s_name;
