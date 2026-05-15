-- STANDARDIZED closure-packet witness artifact for PORT_0004 (spark)
-- Derived deterministically from cases/PORT/PORT_0004/validation/load_witness_spark.sql
-- NOT EXECUTED in this task

-- DRAFT witness load for PORT_0004; not executed in this task
INSERT OVERWRITE patient VALUES
  (1, 'F', 'RA', TIMESTAMP('1980-03-04 00:00:00')),
  (2, 'M', 'RA', TIMESTAMP('1980-11-21 00:00:00')),
  (3, 'F', 'RA', TIMESTAMP('1981-02-09 00:00:00')),
  (4, 'F', 'OA', TIMESTAMP('1980-07-15 00:00:00'));
