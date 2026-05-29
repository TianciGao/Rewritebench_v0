-- PERF_0007 positive rewrite
-- Equivalent to source.sql on PostgreSQL witness data.
-- Rewrite shape: isolate qualifying rows before computing revenue.

select
	sum(extended_discounted_price) as revenue
from
	(
		select
			l_extendedprice * l_discount as extended_discounted_price
		from
			lineitem
		where
			l_shipdate >= date '1995-01-01'
			and l_shipdate < date '1996-01-01'
			and l_discount >= 0.08
			and l_discount <= 0.10
			and l_quantity < 25
	) as qualifying_lineitem;
