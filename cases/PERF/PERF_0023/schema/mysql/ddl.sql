-- PERF_0023 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `lineitem` (
  `l_partkey` int DEFAULT NULL,
  `l_extendedprice` decimal(15,2) DEFAULT NULL,
  `l_discount` decimal(15,2) DEFAULT NULL,
  `l_quantity` decimal(15,2) DEFAULT NULL,
  `l_shipmode` varchar(10) DEFAULT NULL,
  `l_shipinstruct` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `part` (
  `p_partkey` int NOT NULL,
  `p_brand` varchar(10) DEFAULT NULL,
  `p_container` varchar(10) DEFAULT NULL,
  `p_size` int DEFAULT NULL,
  PRIMARY KEY (`p_partkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
