-- PERF_0025 minimal MySQL schema for referenced columns only.

create table supplier (
    s_suppkey integer primary key,
    s_name varchar(25),
    s_nationkey integer
);

create table lineitem (
    l_orderkey integer,
    l_suppkey integer,
    l_receiptdate date,
    l_commitdate date
);

create table orders (
    o_orderkey integer primary key,
    o_orderstatus char(1)
);

create table nation (
    n_nationkey integer primary key,
    n_name varchar(25)
);
