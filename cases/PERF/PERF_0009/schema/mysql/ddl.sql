-- PERF_0009 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `orders` (
  `o_orderkey` int NOT NULL,
  `o_orderpriority` varchar(20) DEFAULT NULL,
  `o_orderdate` date DEFAULT NULL,
  PRIMARY KEY (`o_orderkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `lineitem` (
  `l_orderkey` int DEFAULT NULL,
  `l_commitdate` date DEFAULT NULL,
  `l_receiptdate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
