-- PERF_0020 positive rewrite candidate.
-- Strategy: make joins explicit and express the supplier exclusion as NOT EXISTS.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

select
    part.p_brand,
    part.p_type,
    part.p_size,
    count(distinct partsupp.ps_suppkey) as supplier_cnt
from part
join partsupp
  on part.p_partkey = partsupp.ps_partkey
where
    part.p_brand <> 'Brand#22'
    and part.p_type not like 'SMALL POLISHED%'
    and part.p_size in (42, 9, 18, 29, 36, 6, 24, 17)
    and not exists (
        select 1
        from supplier
        where supplier.s_suppkey = partsupp.ps_suppkey
          and supplier.s_comment like '%Customer%Complaints%'
    )
group by
    part.p_brand,
    part.p_type,
    part.p_size
order by
    supplier_cnt desc,
    part.p_brand,
    part.p_type,
    part.p_size;
