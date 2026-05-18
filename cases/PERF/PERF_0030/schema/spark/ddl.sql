-- PERF_0030 minimal Spark SQL schema for referenced columns only.

create table part (
    p_partkey int,
    p_type string
);

create table lineitem (
    l_partkey int,
    l_extendedprice decimal(12, 2),
    l_discount decimal(12, 2),
    l_shipdate date
);
