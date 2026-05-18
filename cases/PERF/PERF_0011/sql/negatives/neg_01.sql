-- PERF_0011 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but widen the source date window.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    100.00 * sum(case
        when part.p_type like 'PROMO%'
            then lineitem_filtered.l_extendedprice * (1 - lineitem_filtered.l_discount)
        else 0
    end) / sum(lineitem_filtered.l_extendedprice * (1 - lineitem_filtered.l_discount)) as promo_revenue
from (
    select
        l_partkey,
        l_extendedprice,
        l_discount
    from lineitem
    where l_shipdate >= date '1997-03-01'
      and l_shipdate < date '1997-03-01' + interval '2' month
) lineitem_filtered
join part
  on lineitem_filtered.l_partkey = part.p_partkey;
