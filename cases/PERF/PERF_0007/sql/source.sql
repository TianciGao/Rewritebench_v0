-- PERF_0007 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/6.sql
-- Seed: TPC-H Query 6, Forecasting Revenue Change Query
-- Freeze method: manual freeze because local qgen executable was not present.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_6
-- Substitutions: :1 = 1995-01-01, :2 = 0.09, :3 = 25.
-- Row limit directive: :n -1 means no row limit.

-- TPC-H/TPC-R Forecasting Revenue Change Query (Q6)
select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= date '1995-01-01'
	and l_shipdate < date '1995-01-01' + interval '1' year
	and l_discount between 0.09 - 0.01 and 0.09 + 0.01
	and l_quantity < 25;
