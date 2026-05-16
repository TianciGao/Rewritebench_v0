-- PERF_0024 positive rewrite candidate.
-- Strategy: replace comma joins and nested IN predicates with explicit joins and EXISTS while preserving the supplier/part/quantity filters.
-- Equivalence is not yet proven.

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
            and part.p_name like 'pale%'
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
