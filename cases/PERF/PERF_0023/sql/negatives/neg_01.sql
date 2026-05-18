-- PERF_0023 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter one brand predicate.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    sum(lineitem.l_extendedprice * (1 - lineitem.l_discount)) as revenue
from lineitem
join part
  on part.p_partkey = lineitem.l_partkey
where
    (
        part.p_brand = 'Brand#15'
        and part.p_container in ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG')
        and lineitem.l_quantity >= 5 and lineitem.l_quantity <= 15
        and part.p_size between 1 and 5
        and lineitem.l_shipmode in ('AIR', 'AIR REG')
        and lineitem.l_shipinstruct = 'DELIVER IN PERSON'
    )
    or
    (
        part.p_brand = 'Brand#13'
        and part.p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
        and lineitem.l_quantity >= 17 and lineitem.l_quantity <= 27
        and part.p_size between 1 and 10
        and lineitem.l_shipmode in ('AIR', 'AIR REG')
        and lineitem.l_shipinstruct = 'DELIVER IN PERSON'
    )
    or
    (
        part.p_brand = 'Brand#22'
        and part.p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
        and lineitem.l_quantity >= 29 and lineitem.l_quantity <= 39
        and part.p_size between 1 and 15
        and lineitem.l_shipmode in ('AIR', 'AIR REG')
        and lineitem.l_shipinstruct = 'DELIVER IN PERSON'
    );
