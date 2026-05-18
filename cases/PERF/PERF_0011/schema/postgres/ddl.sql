-- PERF_0011 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table lineitem
(
    l_partkey integer,
    l_extendedprice numeric(15,2),
    l_discount numeric(15,2),
    l_shipdate date
);

create table part
(
    p_partkey integer not null,
    p_type varchar(55),
    primary key (p_partkey)
);
