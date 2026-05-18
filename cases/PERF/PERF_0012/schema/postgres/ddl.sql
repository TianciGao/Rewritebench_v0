-- PERF_0012 minimal PostgreSQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

create table part
(
    p_partkey integer not null,
    p_mfgr varchar(25),
    p_size integer,
    p_type varchar(55),
    primary key (p_partkey)
);

create table supplier
(
    s_suppkey integer not null,
    s_name varchar(25),
    s_address varchar(40),
    s_nationkey integer,
    s_phone varchar(15),
    s_acctbal numeric(15,2),
    s_comment varchar(101),
    primary key (s_suppkey)
);

create table partsupp
(
    ps_partkey integer,
    ps_suppkey integer,
    ps_supplycost numeric(15,2)
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
