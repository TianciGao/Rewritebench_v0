-- DRAFT DDL only for PORT_0003; not validated evidence by itself
DROP TABLE IF EXISTS schools;

CREATE TABLE schools (
  gsoffered TEXT,
  longitude DOUBLE -- conservative numeric choice; exact source type may differ
);
