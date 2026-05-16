-- PERF_0013 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey integer not null,
    c_nationkey integer,
    primary key (c_custkey)
);

create table orders
(
    o_orderkey integer not null,
    o_custkey integer,
    o_orderdate date,
    primary key (o_orderkey)
);

create table lineitem
(
    l_orderkey integer,
    l_suppkey integer,
    l_extendedprice numeric(15,2),
    l_discount numeric(15,2)
);

create table supplier
(
    s_suppkey integer not null,
    s_nationkey integer,
    primary key (s_suppkey)
);

create table nation
(
    n_nationkey integer not null,
    n_name varchar(25),
    n_regionkey integer,
    primary key (n_nationkey)
);

create table region
(
    r_regionkey integer not null,
    r_name varchar(25),
    primary key (r_regionkey)
);
