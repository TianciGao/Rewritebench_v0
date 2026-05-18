-- PERF_0021 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/17.sql
-- Seed: TPC-H Query 17, Small-Quantity-Order Revenue Query
-- Freeze method: manual freeze because local qgen executable was not used for this batch.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_17
-- Substitutions: :1 = Brand#31; :2 = JUMBO CASE; :n -1 = no row limit.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Small-Quantity-Order Revenue Query (Q17)
select
    sum(l_extendedprice) / 7.0 as avg_yearly
from
    lineitem,
    part
where
    p_partkey = l_partkey
    and p_brand = 'Brand#31'
    and p_container = 'JUMBO CASE'
    and l_quantity < (
        select
            0.2 * avg(l_quantity)
        from
            lineitem
        where
            l_partkey = p_partkey
    );
