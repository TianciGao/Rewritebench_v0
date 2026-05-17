-- PERF_0029 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.

create table customer
(
    c_custkey integer not null,
    primary key (c_custkey)
);

create table orders
(
    o_orderkey integer not null,
    o_custkey integer,
    o_comment text,
    primary key (o_orderkey)
);
