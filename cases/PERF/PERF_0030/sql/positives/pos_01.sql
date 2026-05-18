-- PERF_0030 positive rewrite candidate.
-- Strategy: precompute extended revenue in a CTE before applying the same aggregate ratio.

with matched_lineitems as (
    select
        part.p_type,
        lineitem.l_extendedprice * (1 - lineitem.l_discount) as revenue
    from lineitem
    join part
      on lineitem.l_partkey = part.p_partkey
    where
        lineitem.l_shipdate >= date '1997-03-01'
        and lineitem.l_shipdate < date '1997-03-01' + interval '1' month
)
select
    100.00 * sum(case
        when substring(p_type from 1 for 5) = 'PROMO' then revenue
        else 0
    end) / sum(revenue) as promo_revenue
from
    matched_lineitems;
