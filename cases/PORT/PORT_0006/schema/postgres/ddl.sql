-- DRAFT DDL only for PORT_0006; not executed
CREATE TABLE loan (
  status TEXT,
  account_id INTEGER,
  amount DOUBLE PRECISION -- conservative numeric choice; exact source type may differ
);
