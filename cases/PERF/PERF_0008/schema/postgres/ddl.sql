-- PERF_0008 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey integer not null,
    c_mktsegment varchar(25),
    primary key (c_custkey)
);

create table orders
(
    o_orderkey integer not null,
    o_custkey integer,
    o_orderdate date,
    o_shippriority integer,
    primary key (o_orderkey)
);

create table lineitem
(
    l_orderkey integer,
    l_extendedprice numeric(15,2),
    l_discount numeric(15,2),
    l_shipdate date
);
