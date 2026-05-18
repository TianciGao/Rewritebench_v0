-- PERF_0011 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/14.sql
-- Seed: TPC-H Query 14, Promotion Effect Query
-- Freeze method: manual freeze because local qgen executable was not present.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_14
-- Substitutions: :1 = 1997-03-01; :n -1 = no row limit.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Promotion Effect Query (Q14)
select
    100.00 * sum(case
        when p_type like 'PROMO%'
            then l_extendedprice * (1 - l_discount)
        else 0
    end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from
    lineitem,
    part
where
    l_partkey = p_partkey
    and l_shipdate >= date '1997-03-01'
    and l_shipdate < date '1997-03-01' + interval '1' month;
