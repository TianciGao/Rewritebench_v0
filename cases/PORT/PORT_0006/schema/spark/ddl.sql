-- DRAFT DDL only for PORT_0006; not executed as validated evidence.
-- Conservative numeric choice; exact source type may differ.
DROP TABLE IF EXISTS loan;
CREATE TABLE loan (
  status STRING,
  account_id INT,
  amount DOUBLE
);
