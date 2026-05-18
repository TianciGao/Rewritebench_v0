-- PERF_0031 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/variants/15a.sql
-- Seed: TPC-H Query 15 Variant A, Top Supplier Query
-- Freeze method: manual freeze using the existing Q15 parameter line.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_15
-- Substitutions: :1 = 1994-06-01; :n -1 = no row limit.
-- No MySQL/Spark, plan, admission, or promotion claim is made by this file.

with revenue (supplier_no, total_revenue) as (
    select
        l_suppkey,
        sum(l_extendedprice * (1 - l_discount))
    from
        lineitem
    where
        l_shipdate >= date '1994-06-01'
        and l_shipdate < date '1994-06-01' + interval '3' month
    group by
        l_suppkey
)
select
    s_suppkey,
    s_name,
    s_address,
    s_phone,
    total_revenue
from
    supplier,
    revenue
where
    s_suppkey = supplier_no
    and total_revenue = (
        select
            max(total_revenue)
        from
            revenue
    )
order by
    s_suppkey;
