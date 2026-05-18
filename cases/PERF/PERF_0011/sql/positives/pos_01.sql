-- PERF_0011 positive rewrite candidate.
-- Strategy: make the join explicit and push the fixed date window into a derived lineitem table.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

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
      and l_shipdate < date '1997-03-01' + interval '1' month
) lineitem_filtered
join part
  on lineitem_filtered.l_partkey = part.p_partkey;
