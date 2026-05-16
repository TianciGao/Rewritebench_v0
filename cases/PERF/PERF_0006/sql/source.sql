-- PERF_0006 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/1.sql
-- Seed: TPC-H Query 1, Pricing Summary Report Query
-- Freeze method: manual freeze because local qgen executable was not present.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_1
-- Substitution: :1 = 96 days.
-- Frozen cutoff: DATE '1998-08-27' = DATE '1998-12-01' - 96 days.
-- No execution, equivalence, rewrite, or validation claim is made by this file.

-- TPC-H/TPC-R Pricing Summary Report Query (Q1)
select
	l_returnflag,
	l_linestatus,
	sum(l_quantity) as sum_qty,
	sum(l_extendedprice) as sum_base_price,
	sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
	sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
	avg(l_quantity) as avg_qty,
	avg(l_extendedprice) as avg_price,
	avg(l_discount) as avg_disc,
	count(*) as count_order
from
	lineitem
where
	l_shipdate <= date '1998-08-27'
group by
	l_returnflag,
	l_linestatus
order by
	l_returnflag,
	l_linestatus;
