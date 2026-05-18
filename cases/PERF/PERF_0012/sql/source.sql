-- PERF_0012 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/2.sql
-- Seed: TPC-H Query 2, Minimum Cost Supplier Query
-- Freeze method: manual freeze because local qgen executable was not present.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_2
-- Substitutions: :1 = 25; :2 = TIN; :3 = MIDDLE EAST; :n 100 = LIMIT 100.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Minimum Cost Supplier Query (Q2)
select
    s_acctbal,
    s_name,
    n_name,
    p_partkey,
    p_mfgr,
    s_address,
    s_phone,
    s_comment
from
    part,
    supplier,
    partsupp,
    nation,
    region
where
    p_partkey = ps_partkey
    and s_suppkey = ps_suppkey
    and p_size = 25
    and p_type like '%TIN'
    and s_nationkey = n_nationkey
    and n_regionkey = r_regionkey
    and r_name = 'MIDDLE EAST'
    and ps_supplycost = (
        select
            min(ps_supplycost)
        from
            partsupp,
            supplier,
            nation,
            region
        where
            p_partkey = ps_partkey
            and s_suppkey = ps_suppkey
            and s_nationkey = n_nationkey
            and n_regionkey = r_regionkey
            and r_name = 'MIDDLE EAST'
    )
order by
    s_acctbal desc,
    n_name,
    s_name,
    p_partkey
limit 100;
