-- PERF_0019 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table customer
(
    c_custkey integer not null,
    primary key (c_custkey)
);

create table orders
(
    o_orderkey integer not null,
    o_custkey integer,
    o_comment varchar(79),
    primary key (o_orderkey)
);
