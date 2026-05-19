-- PERF_0006 positive rewrite
-- Equivalent to source.sql on PostgreSQL witness data.
-- Rewrite shape: isolate the source filter in a derived relation before aggregation.

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
	(
		select
			l_returnflag,
			l_linestatus,
			l_quantity,
			l_extendedprice,
			l_discount,
			l_tax
		from
			lineitem
		where
			l_shipdate <= date '1998-08-27'
	) as filtered_lineitem
group by
	l_returnflag,
	l_linestatus
order by
	l_returnflag,
	l_linestatus;
