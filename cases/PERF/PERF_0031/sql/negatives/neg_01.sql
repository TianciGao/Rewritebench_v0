-- PERF_0031 negative rewrite candidate.
-- Strategy: incorrectly select the minimum supplier revenue rather than the maximum.

with supplier_revenue as (
    select
        lineitem.l_suppkey as supplier_no,
        sum(lineitem.l_extendedprice * (1 - lineitem.l_discount)) as total_revenue
    from lineitem
    where
        lineitem.l_shipdate >= date '1994-06-01'
        and lineitem.l_shipdate < date '1994-06-01' + interval '3' month
    group by
        lineitem.l_suppkey
)
select
    supplier.s_suppkey,
    supplier.s_name,
    supplier.s_address,
    supplier.s_phone,
    supplier_revenue.total_revenue
from supplier
join supplier_revenue
  on supplier.s_suppkey = supplier_revenue.supplier_no
where
    supplier_revenue.total_revenue = (
        select min(total_revenue)
        from supplier_revenue
    )
order by
    supplier.s_suppkey;
