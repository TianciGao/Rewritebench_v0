-- DRAFT DDL only for PORT_0004; not executed
CREATE TABLE patient (
  id INTEGER,
  sex TEXT,
  diagnosis TEXT,
  birthday TIMESTAMP -- conservative choice; source may also tolerate DATE-level storage
);
