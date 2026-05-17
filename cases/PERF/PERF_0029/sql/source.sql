-- PERF_0029 source layer
-- Source registry row: SRC_001 (TPC-H)
-- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/variants/13a.sql
-- Seed: TPC-H Query 13 Variant A, Customer Distribution Query
-- Freeze method: manual freeze using the existing Q13 parameter line.
-- Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_13
-- Substitutions: :1 = express; :2 = deposits; :n -1 = no row limit.
-- No MySQL/Spark, plan, admission, or promotion claim is made by this file.

create view orders_per_cust (custkey, ordercount) as
    select
        c_custkey,
        count(o_orderkey)
    from
        customer left outer join orders on
            c_custkey = o_custkey
            and o_comment not like '%express%deposits%'
    group by
        c_custkey;

select
    ordercount,
    count(*) as custdist
from
    orders_per_cust
group by
    ordercount
order by
    custdist desc,
    ordercount desc;

drop view orders_per_cust;
