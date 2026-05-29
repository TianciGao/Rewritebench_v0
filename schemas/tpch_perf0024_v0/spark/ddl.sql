-- PERF_0024 minimal Spark SQL schema for referenced columns only.

create table supplier (
    s_suppkey int,
    s_name string,
    s_address string,
    s_nationkey int
);

create table nation (
    n_nationkey int,
    n_name string
);

create table partsupp (
    ps_partkey int,
    ps_suppkey int,
    ps_availqty int
);

create table part (
    p_partkey int,
    p_name string
);

create table lineitem (
    l_partkey int,
    l_suppkey int,
    l_quantity decimal(15, 2),
    l_shipdate date
);
