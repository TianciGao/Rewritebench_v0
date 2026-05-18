-- PERF_0022 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/18.sql
-- Seed: TPC-H Query 18, Large Volume Customer Query
-- Freeze method: manual freeze because local qgen executable was not used for this batch.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_18
-- Substitutions: :1 = 312; :n 100 = LIMIT 100.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Large Volume Customer Query (Q18)
select
    c_name,
    c_custkey,
    o_orderkey,
    o_orderdate,
    o_totalprice,
    sum(l_quantity)
from
    customer,
    orders,
    lineitem
where
    o_orderkey in (
        select
            l_orderkey
        from
            lineitem
        group by
            l_orderkey
        having
            sum(l_quantity) > 312
    )
    and c_custkey = o_custkey
    and o_orderkey = l_orderkey
group by
    c_name,
    c_custkey,
    o_orderkey,
    o_orderdate,
    o_totalprice
order by
    o_totalprice desc,
    o_orderdate
limit 100;
