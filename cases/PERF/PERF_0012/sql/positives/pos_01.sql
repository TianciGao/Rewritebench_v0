-- PERF_0012 positive rewrite candidate.
-- Strategy: make joins explicit and precompute the regional minimum supply cost per part.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

select
    supplier.s_acctbal,
    supplier.s_name,
    nation.n_name,
    part.p_partkey,
    part.p_mfgr,
    supplier.s_address,
    supplier.s_phone,
    supplier.s_comment
from part
join partsupp
  on part.p_partkey = partsupp.ps_partkey
join supplier
  on supplier.s_suppkey = partsupp.ps_suppkey
join nation
  on supplier.s_nationkey = nation.n_nationkey
join region
  on nation.n_regionkey = region.r_regionkey
join (
    select
        partsupp.ps_partkey,
        min(partsupp.ps_supplycost) as min_supplycost
    from partsupp
    join supplier
      on supplier.s_suppkey = partsupp.ps_suppkey
    join nation
      on supplier.s_nationkey = nation.n_nationkey
    join region
      on nation.n_regionkey = region.r_regionkey
    where region.r_name = 'MIDDLE EAST'
    group by
        partsupp.ps_partkey
) regional_min_supply
  on regional_min_supply.ps_partkey = part.p_partkey
 and regional_min_supply.min_supplycost = partsupp.ps_supplycost
where
    part.p_size = 25
    and part.p_type like '%TIN'
    and region.r_name = 'MIDDLE EAST'
order by
    supplier.s_acctbal desc,
    nation.n_name,
    supplier.s_name,
    part.p_partkey
limit 100;
