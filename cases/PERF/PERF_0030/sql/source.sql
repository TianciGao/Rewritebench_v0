-- PERF_0030 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/variants/14a.sql
-- Seed: TPC-H Query 14 Variant A, Promotion Effect Query
-- Freeze method: manual freeze using the existing Q14 parameter line.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_14
-- Substitutions: :1 = 1997-03-01; :n -1 = no row limit.
-- No MySQL/Spark, plan, admission, or promotion claim is made by this file.

select
    100.00 * sum(case
        when substring(p_type from 1 for 5) = 'PROMO'
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
