-- PERF_0025 minimal Spark SQL schema for referenced columns only.

create table supplier (
    s_suppkey int,
    s_name string,
    s_nationkey int
);

create table lineitem (
    l_orderkey int,
    l_suppkey int,
    l_receiptdate date,
    l_commitdate date
);

create table orders (
    o_orderkey int,
    o_orderstatus string
);

create table nation (
    n_nationkey int,
    n_name string
);
