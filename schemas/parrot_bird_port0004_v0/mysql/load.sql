-- DRAFT witness fixture for PORT_0004; not validated evidence by itself
DROP TABLE IF EXISTS patient;

CREATE TABLE patient (
  id INT,
  sex TEXT,
  diagnosis TEXT,
  birthday DATETIME -- conservative choice; source may also tolerate DATE-level storage
);

INSERT INTO patient (id, sex, diagnosis, birthday) VALUES
  (1, 'F', 'RA', '1980-03-04'),
  (2, 'M', 'RA', '1980-11-21'),
  (3, 'F', 'RA', '1981-02-09'),
  (4, 'F', 'OA', '1980-07-15');
