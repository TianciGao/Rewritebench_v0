-- PERF_0008 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/3.sql
-- Seed: TPC-H Query 3, Shipping Priority Query
-- Freeze method: manual freeze because local qgen executable was not present.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_3
-- Substitutions: :1 = MACHINERY; :2 = 1995-03-27; :n 10 = LIMIT 10.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Shipping Priority Query (Q3)
select
	l_orderkey,
	sum(l_extendedprice * (1 - l_discount)) as revenue,
	o_orderdate,
	o_shippriority
from
	customer,
	orders,
	lineitem
where
	c_mktsegment = 'MACHINERY'
	and c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate < date '1995-03-27'
	and l_shipdate > date '1995-03-27'
group by
	l_orderkey,
	o_orderdate,
	o_shippriority
order by
	revenue desc,
	o_orderdate
limit 10;
