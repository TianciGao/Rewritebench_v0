-- DRAFT DDL only for PORT_0004; not executed
DROP TABLE IF EXISTS patient;

CREATE TABLE patient (
  id INT,
  sex STRING,
  diagnosis STRING,
  birthday TIMESTAMP
);
