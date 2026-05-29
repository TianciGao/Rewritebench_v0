-- DRAFT witness fixture for PORT_0003; not validated evidence by itself
DROP TABLE IF EXISTS schools;

CREATE TABLE schools (
  gsoffered TEXT,
  longitude DOUBLE -- conservative numeric choice; exact source type may differ
);

INSERT INTO schools (gsoffered, longitude) VALUES
  ('north-max', 120.0),
  ('south-mid', -45.0),
  ('near-origin', 5.0),
  ('unknown', NULL);
