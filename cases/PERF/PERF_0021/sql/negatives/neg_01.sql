-- PERF_0021 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the part container filter.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    sum(lineitem.l_extendedprice) / 7.0 as avg_yearly
from part
join lineitem
  on part.p_partkey = lineitem.l_partkey
join (
    select
        l_partkey,
        avg(l_quantity) as avg_quantity
    from lineitem
    group by
        l_partkey
) part_quantity
  on part_quantity.l_partkey = part.p_partkey
where
    part.p_brand = 'Brand#31'
    and part.p_container = 'JUMBO BOX'
    and lineitem.l_quantity < 0.2 * part_quantity.avg_quantity;
