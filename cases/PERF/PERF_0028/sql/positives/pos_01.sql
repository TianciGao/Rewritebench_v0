-- PERF_0028 positive rewrite candidate.
-- Strategy: use explicit join syntax and IN predicates for the priority buckets.

select
    lineitem.l_shipmode,
    sum(case
        when orders.o_orderpriority in ('1-URGENT', '2-HIGH') then 1
        else 0
    end) as high_line_count,
    sum(case
        when orders.o_orderpriority not in ('1-URGENT', '2-HIGH') then 1
        else 0
    end) as low_line_count
from orders
join lineitem
  on orders.o_orderkey = lineitem.l_orderkey
where
    lineitem.l_shipmode in ('REG AIR', 'RAIL')
    and lineitem.l_commitdate < lineitem.l_receiptdate
    and lineitem.l_shipdate < lineitem.l_commitdate
    and lineitem.l_receiptdate >= date '1993-01-01'
    and lineitem.l_receiptdate < date '1993-01-01' + interval '1' year
group by
    lineitem.l_shipmode
order by
    lineitem.l_shipmode;
