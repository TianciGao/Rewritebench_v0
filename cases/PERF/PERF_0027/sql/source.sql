-- PERF_0027 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/variants/8a.sql
-- Seed: TPC-H Query 8 Variant A, National Market Share Query
-- Freeze method: manual freeze using the existing Q8 parameter line.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_8
-- Substitutions: :1 = IRAN; :2 = MIDDLE EAST; :3 = MEDIUM POLISHED STEEL; :n -1 = no row limit.
-- No MySQL/Spark, plan, admission, or promotion claim is made by this file.

select
    o_year,
    sum(case
        when nation = 'IRAN' then volume
        else 0
    end) / sum(volume) as mkt_share
from (
    select
        extract(year from o_orderdate) as o_year,
        l_extendedprice * (1 - l_discount) as volume,
        n2.n_name as nation
    from
        part,
        supplier,
        lineitem,
        orders,
        customer,
        nation n1,
        nation n2,
        region
    where
        p_partkey = l_partkey
        and s_suppkey = l_suppkey
        and l_orderkey = o_orderkey
        and o_custkey = c_custkey
        and c_nationkey = n1.n_nationkey
        and n1.n_regionkey = r_regionkey
        and r_name = 'MIDDLE EAST'
        and s_nationkey = n2.n_nationkey
        and o_orderdate between date '1995-01-01' and date '1996-12-31'
        and p_type = 'MEDIUM POLISHED STEEL'
) all_nations
group by
    o_year
order by
    o_year;
