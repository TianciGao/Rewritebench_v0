-- PERF_0010 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/12.sql
-- Seed: TPC-H Query 12, Shipping Modes and Order Priority Query
-- Freeze method: manual freeze because local qgen executable was not present.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_12
-- Substitutions: :1 = REG AIR; :2 = RAIL; :3 = 1993-01-01; :n -1 = no row limit.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Shipping Modes and Order Priority Query (Q12)
select
    l_shipmode,
    sum(case
        when o_orderpriority = '1-URGENT'
            or o_orderpriority = '2-HIGH'
            then 1
        else 0
    end) as high_line_count,
    sum(case
        when o_orderpriority <> '1-URGENT'
            and o_orderpriority <> '2-HIGH'
            then 1
        else 0
    end) as low_line_count
from
    orders,
    lineitem
where
    o_orderkey = l_orderkey
    and l_shipmode in ('REG AIR', 'RAIL')
    and l_commitdate < l_receiptdate
    and l_shipdate < l_commitdate
    and l_receiptdate >= date '1993-01-01'
    and l_receiptdate < date '1993-01-01' + interval '1' year
group by
    l_shipmode
order by
    l_shipmode;
