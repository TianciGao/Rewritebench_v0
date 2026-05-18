-- PERF_0030 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.

create table part
(
    p_partkey integer not null,
    p_type varchar(100),
    primary key (p_partkey)
);

create table lineitem
(
    l_partkey integer,
    l_extendedprice numeric(12, 2),
    l_discount numeric(12, 2),
    l_shipdate date
);
