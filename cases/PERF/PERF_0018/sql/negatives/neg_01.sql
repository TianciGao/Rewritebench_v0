-- PERF_0018 negative rewrite candidate.
-- Strategy: retain the positive rewrite shape but alter the nation predicate.
-- This is a plausible semantic-divergence candidate, not a proven divergence claim.

select
    partsupp.ps_partkey,
    sum(partsupp.ps_supplycost * partsupp.ps_availqty) as value
from partsupp
join supplier
  on partsupp.ps_suppkey = supplier.s_suppkey
join nation
  on supplier.s_nationkey = nation.n_nationkey
cross join (
    select
        sum(partsupp.ps_supplycost * partsupp.ps_availqty) * 0.0001000000 as threshold_value
    from partsupp
    join supplier
      on partsupp.ps_suppkey = supplier.s_suppkey
    join nation
      on supplier.s_nationkey = nation.n_nationkey
    where nation.n_name = 'FRANCE'
) national_threshold
where
    nation.n_name = 'FRANCE'
group by
    partsupp.ps_partkey,
    national_threshold.threshold_value
having
    sum(partsupp.ps_supplycost * partsupp.ps_availqty) > national_threshold.threshold_value
order by
    value desc;
