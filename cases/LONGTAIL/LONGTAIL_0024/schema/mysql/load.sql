INSERT INTO Posts VALUES
  (301, 'Disk cleanup tips', 10, 1000),
  (302, 'Network latency issue', 8, 800),
  (303, 'Printer setup help', 5, 400),
  (304, 'Backup strategy', 7, 600),
  (305, 'Single-edit post', 2, 120);

INSERT INTO PostHistory VALUES
  (1, 301, 1, 2, '2020-03-01 08:00:00', 'initial revision'),
  (2, 301, 1, 5, '2020-03-01 09:00:00', 'follow-up edit'),
  (3, 301, 2, 5, '2020-03-01 10:00:00', 'peer edit'),
  (4, 302, 2, 2, '2020-03-02 08:00:00', 'initial revision'),
  (5, 302, 2, 5, '2020-03-02 09:00:00', 'same editor follow-up'),
  (6, 303, 3, 2, '2020-03-03 08:00:00', 'initial revision'),
  (7, 304, 4, 2, '2020-03-01 07:00:00', 'initial revision'),
  (8, 304, 4, 5, '2020-03-01 07:30:00', 'formatting edit'),
  (9, 304, 4, 5, '2020-03-01 08:00:00', 'cleanup edit'),
  (10, 305, 1, 2, '2020-03-04 08:00:00', 'single revision');
