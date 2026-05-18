-- PERF_0027 minimal Spark SQL schema for referenced columns only.

create table part (
    p_partkey int,
    p_type string
);

create table supplier (
    s_suppkey int,
    s_nationkey int
);

create table lineitem (
    l_partkey int,
    l_suppkey int,
    l_orderkey int,
    l_extendedprice decimal(12, 2),
    l_discount decimal(12, 2)
);

create table orders (
    o_orderkey int,
    o_custkey int,
    o_orderdate date
);

create table customer (
    c_custkey int,
    c_nationkey int
);

create table nation (
    n_nationkey int,
    n_name string,
    n_regionkey int
);

create table region (
    r_regionkey int,
    r_name string
);
