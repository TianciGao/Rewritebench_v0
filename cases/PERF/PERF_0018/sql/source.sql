-- PERF_0018 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/11.sql
-- Seed: TPC-H Query 11, Important Stock Identification Query
-- Freeze method: manual freeze because local qgen executable was not used for this batch.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_11
-- Substitutions: :1 = EGYPT; :2 = 0.0001000000; :n -1 = no row limit.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Important Stock Identification Query (Q11)
select
    ps_partkey,
    sum(ps_supplycost * ps_availqty) as value
from
    partsupp,
    supplier,
    nation
where
    ps_suppkey = s_suppkey
    and s_nationkey = n_nationkey
    and n_name = 'EGYPT'
group by
    ps_partkey
having
    sum(ps_supplycost * ps_availqty) > (
        select
            sum(ps_supplycost * ps_availqty) * 0.0001000000
        from
            partsupp,
            supplier,
            nation
        where
            ps_suppkey = s_suppkey
            and s_nationkey = n_nationkey
            and n_name = 'EGYPT'
    )
order by
    value desc;
