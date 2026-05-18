-- PERF_0016 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `part` (
  `p_partkey` int NOT NULL,
  `p_name` varchar(55) DEFAULT NULL,
  PRIMARY KEY (`p_partkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `supplier` (
  `s_suppkey` int NOT NULL,
  `s_nationkey` int DEFAULT NULL,
  PRIMARY KEY (`s_suppkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `lineitem` (
  `l_partkey` int DEFAULT NULL,
  `l_suppkey` int DEFAULT NULL,
  `l_orderkey` int DEFAULT NULL,
  `l_extendedprice` decimal(15,2) DEFAULT NULL,
  `l_discount` decimal(15,2) DEFAULT NULL,
  `l_quantity` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `partsupp` (
  `ps_partkey` int DEFAULT NULL,
  `ps_suppkey` int DEFAULT NULL,
  `ps_supplycost` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `orders` (
  `o_orderkey` int NOT NULL,
  `o_orderdate` date DEFAULT NULL,
  PRIMARY KEY (`o_orderkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `nation` (
  `n_nationkey` int NOT NULL,
  `n_name` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`n_nationkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
