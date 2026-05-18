-- PERF_0021 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table lineitem
(
    l_partkey integer,
    l_extendedprice numeric(15,2),
    l_quantity numeric(15,2)
);

create table part
(
    p_partkey integer not null,
    p_brand varchar(10),
    p_container varchar(10),
    primary key (p_partkey)
);
