-- PERF_0024 source query.
-- TPC-H Q20 frozen from ref_data/1/subparam_20.
-- Substitutions: :1 = 'pale'; :2 = DATE '1997-01-01'; :3 = 'BRAZIL'; :n = -1.

select
    s_name,
    s_address
from
    supplier,
    nation
where
    s_suppkey in (
        select
            ps_suppkey
        from
            partsupp
        where
            ps_partkey in (
                select
                    p_partkey
                from
                    part
                where
                    p_name like 'pale%'
            )
            and ps_availqty > (
                select
                    0.5 * sum(l_quantity)
                from
                    lineitem
                where
                    l_partkey = ps_partkey
                    and l_suppkey = ps_suppkey
                    and l_shipdate >= date '1997-01-01'
                    and l_shipdate < date '1997-01-01' + interval '1' year
            )
    )
    and s_nationkey = n_nationkey
    and n_name = 'BRAZIL'
order by
    s_name;
