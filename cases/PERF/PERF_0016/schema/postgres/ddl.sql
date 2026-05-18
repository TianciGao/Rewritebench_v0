-- PERF_0016 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table part
(
    p_partkey integer not null,
    p_name varchar(55),
    primary key (p_partkey)
);

create table supplier
(
    s_suppkey integer not null,
    s_nationkey integer,
    primary key (s_suppkey)
);

create table lineitem
(
    l_partkey integer,
    l_suppkey integer,
    l_orderkey integer,
    l_extendedprice numeric(15,2),
    l_discount numeric(15,2),
    l_quantity numeric(15,2)
);

create table partsupp
(
    ps_partkey integer,
    ps_suppkey integer,
    ps_supplycost numeric(15,2)
);

create table orders
(
    o_orderkey integer not null,
    o_orderdate date,
    primary key (o_orderkey)
);

create table nation
(
    n_nationkey integer not null,
    n_name varchar(25),
    primary key (n_nationkey)
);
