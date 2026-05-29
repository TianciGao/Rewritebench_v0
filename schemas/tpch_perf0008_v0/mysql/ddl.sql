-- PERF_0008 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `customer` (
  `c_custkey` int NOT NULL,
  `c_mktsegment` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`c_custkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `orders` (
  `o_orderkey` int NOT NULL,
  `o_custkey` int DEFAULT NULL,
  `o_orderdate` date DEFAULT NULL,
  `o_shippriority` int DEFAULT NULL,
  PRIMARY KEY (`o_orderkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `lineitem` (
  `l_orderkey` int DEFAULT NULL,
  `l_extendedprice` decimal(15,2) DEFAULT NULL,
  `l_discount` decimal(15,2) DEFAULT NULL,
  `l_shipdate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
