-- DRAFT DDL only for PORT_0006; not validated evidence by itself
DROP TABLE IF EXISTS loan;

CREATE TABLE loan (
  status TEXT,
  account_id INT,
  amount DOUBLE -- conservative numeric choice; exact source type may differ
);
