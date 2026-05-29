-- PERF_0024 minimal PostgreSQL schema for referenced columns only.

create table supplier (
    s_suppkey integer primary key,
    s_name varchar(25),
    s_address varchar(40),
    s_nationkey integer
);

create table nation (
    n_nationkey integer primary key,
    n_name varchar(25)
);

create table partsupp (
    ps_partkey integer,
    ps_suppkey integer,
    ps_availqty integer
);

create table part (
    p_partkey integer primary key,
    p_name varchar(55)
);

create table lineitem (
    l_partkey integer,
    l_suppkey integer,
    l_quantity numeric(15, 2),
    l_shipdate date
);
