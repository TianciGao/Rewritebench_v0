-- PERF_0020 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/16.sql
-- Seed: TPC-H Query 16, Parts/Supplier Relationship Query
-- Freeze method: manual freeze because local qgen executable was not used for this batch.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_16
-- Substitutions: :1 = Brand#22; :2 = SMALL POLISHED; :3..:10 = 42, 9, 18, 29, 36, 6, 24, 17; :n -1 = no row limit.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Parts/Supplier Relationship Query (Q16)
select
    p_brand,
    p_type,
    p_size,
    count(distinct ps_suppkey) as supplier_cnt
from
    partsupp,
    part
where
    p_partkey = ps_partkey
    and p_brand <> 'Brand#22'
    and p_type not like 'SMALL POLISHED%'
    and p_size in (42, 9, 18, 29, 36, 6, 24, 17)
    and ps_suppkey not in (
        select
            s_suppkey
        from
            supplier
        where
            s_comment like '%Customer%Complaints%'
    )
group by
    p_brand,
    p_type,
    p_size
order by
    supplier_cnt desc,
    p_brand,
    p_type,
    p_size;
