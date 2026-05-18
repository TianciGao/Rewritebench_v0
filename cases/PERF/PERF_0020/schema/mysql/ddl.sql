-- PERF_0020 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `partsupp` (
  `ps_partkey` int DEFAULT NULL,
  `ps_suppkey` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `part` (
  `p_partkey` int NOT NULL,
  `p_brand` varchar(10) DEFAULT NULL,
  `p_type` varchar(55) DEFAULT NULL,
  `p_size` int DEFAULT NULL,
  PRIMARY KEY (`p_partkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `supplier` (
  `s_suppkey` int NOT NULL,
  `s_comment` varchar(101) DEFAULT NULL,
  PRIMARY KEY (`s_suppkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
