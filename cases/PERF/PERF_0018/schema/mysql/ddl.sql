-- PERF_0018 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `partsupp` (
  `ps_partkey` int DEFAULT NULL,
  `ps_suppkey` int DEFAULT NULL,
  `ps_supplycost` decimal(15,2) DEFAULT NULL,
  `ps_availqty` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `supplier` (
  `s_suppkey` int NOT NULL,
  `s_nationkey` int DEFAULT NULL,
  PRIMARY KEY (`s_suppkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `nation` (
  `n_nationkey` int NOT NULL,
  `n_name` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`n_nationkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
