-- PERF_0009 negative rewrite candidate.
-- Strategy: retain the semi-join shape but loosen the lineitem date predicate.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    orders.o_orderpriority,
    count(*) as order_count
from orders
join (
    select distinct
        l_orderkey
    from lineitem
    where l_commitdate <= l_receiptdate
) qualifying_lineitem_orders
  on qualifying_lineitem_orders.l_orderkey = orders.o_orderkey
where
    orders.o_orderdate >= date '1996-11-01'
    and orders.o_orderdate < date '1996-11-01' + interval '3' month
group by
    orders.o_orderpriority
order by
    orders.o_orderpriority;
