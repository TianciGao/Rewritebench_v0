-- PERF_0012 minimal MySQL schema.
-- Covers only tables and columns referenced by source.sql and rewrite candidates.
-- No data rows, load path, execution success, or validation result is implied.

CREATE TABLE `part` (
  `p_partkey` int NOT NULL,
  `p_mfgr` varchar(25) DEFAULT NULL,
  `p_size` int DEFAULT NULL,
  `p_type` varchar(55) DEFAULT NULL,
  PRIMARY KEY (`p_partkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `supplier` (
  `s_suppkey` int NOT NULL,
  `s_name` varchar(25) DEFAULT NULL,
  `s_address` varchar(40) DEFAULT NULL,
  `s_nationkey` int DEFAULT NULL,
  `s_phone` varchar(15) DEFAULT NULL,
  `s_acctbal` decimal(15,2) DEFAULT NULL,
  `s_comment` varchar(101) DEFAULT NULL,
  PRIMARY KEY (`s_suppkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `partsupp` (
  `ps_partkey` int DEFAULT NULL,
  `ps_suppkey` int DEFAULT NULL,
  `ps_supplycost` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `nation` (
  `n_nationkey` int NOT NULL,
  `n_name` varchar(25) DEFAULT NULL,
  `n_regionkey` int DEFAULT NULL,
  PRIMARY KEY (`n_nationkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `region` (
  `r_regionkey` int NOT NULL,
  `r_name` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`r_regionkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
