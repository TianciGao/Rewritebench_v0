-- PERF_0010 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter one selected ship mode.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    lineitem_filtered.l_shipmode,
    sum(case
        when orders.o_orderpriority = '1-URGENT'
            or orders.o_orderpriority = '2-HIGH'
            then 1
        else 0
    end) as high_line_count,
    sum(case
        when orders.o_orderpriority <> '1-URGENT'
            and orders.o_orderpriority <> '2-HIGH'
            then 1
        else 0
    end) as low_line_count
from orders
join (
    select
        l_orderkey,
        l_shipmode
    from lineitem
    where l_shipmode in ('REG AIR', 'SHIP')
      and l_commitdate < l_receiptdate
      and l_shipdate < l_commitdate
      and l_receiptdate >= date '1993-01-01'
      and l_receiptdate < date '1993-01-01' + interval '1' year
) lineitem_filtered
  on orders.o_orderkey = lineitem_filtered.l_orderkey
group by
    lineitem_filtered.l_shipmode
order by
    lineitem_filtered.l_shipmode;
