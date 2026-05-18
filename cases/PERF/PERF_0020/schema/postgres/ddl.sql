-- PERF_0020 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table partsupp
(
    ps_partkey integer,
    ps_suppkey integer
);

create table part
(
    p_partkey integer not null,
    p_brand varchar(10),
    p_type varchar(55),
    p_size integer,
    primary key (p_partkey)
);

create table supplier
(
    s_suppkey integer not null,
    s_comment varchar(101),
    primary key (s_suppkey)
);
