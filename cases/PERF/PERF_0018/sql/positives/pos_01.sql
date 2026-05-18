-- PERF_0018 positive rewrite candidate.
-- Strategy: make joins explicit and precompute the national total value threshold.
-- This is a plausible result-preserving candidate, not a proven equivalence claim.

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
    where nation.n_name = 'EGYPT'
) national_threshold
where
    nation.n_name = 'EGYPT'
group by
    partsupp.ps_partkey,
    national_threshold.threshold_value
having
    sum(partsupp.ps_supplycost * partsupp.ps_availqty) > national_threshold.threshold_value
order by
    value desc;
