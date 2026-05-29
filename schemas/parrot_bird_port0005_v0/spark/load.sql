-- DRAFT witness fixture for PORT_0005; not validated evidence by itself
DROP TABLE IF EXISTS drivers;

CREATE TABLE drivers (
  nationality STRING,
  dob TIMESTAMP
);

INSERT INTO drivers VALUES
  ('argentina_null', NULL),
  ('japan_earliest', TIMESTAMP '1979-07-04 00:00:00'),
  ('canada_mid', TIMESTAMP '1985-02-11 00:00:00'),
  ('brazil_latest', TIMESTAMP '1992-09-30 00:00:00');
