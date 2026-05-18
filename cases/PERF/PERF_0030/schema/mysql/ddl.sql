-- PERF_0030 minimal MySQL schema for referenced columns only.

create table part (
    p_partkey integer primary key,
    p_type varchar(100)
);

create table lineitem (
    l_partkey integer,
    l_extendedprice decimal(12, 2),
    l_discount decimal(12, 2),
    l_shipdate date
);
