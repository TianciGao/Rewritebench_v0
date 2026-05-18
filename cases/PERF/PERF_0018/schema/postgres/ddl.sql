-- PERF_0018 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table partsupp
(
    ps_partkey integer,
    ps_suppkey integer,
    ps_supplycost numeric(15,2),
    ps_availqty integer
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
    primary key (n_nationkey)
);
