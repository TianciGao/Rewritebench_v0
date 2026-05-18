-- PERF_0027 minimal MySQL schema for referenced columns only.

create table part (
    p_partkey integer primary key,
    p_type varchar(100)
);

create table supplier (
    s_suppkey integer primary key,
    s_nationkey integer
);

create table lineitem (
    l_partkey integer,
    l_suppkey integer,
    l_orderkey integer,
    l_extendedprice decimal(12, 2),
    l_discount decimal(12, 2)
);

create table orders (
    o_orderkey integer primary key,
    o_custkey integer,
    o_orderdate date
);

create table customer (
    c_custkey integer primary key,
    c_nationkey integer
);

create table nation (
    n_nationkey integer primary key,
    n_name varchar(50),
    n_regionkey integer
);

create table region (
    r_regionkey integer primary key,
    r_name varchar(50)
);
