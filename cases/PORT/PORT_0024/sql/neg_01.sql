SELECT 100.0 * SUM(CASE WHEN istextless = 0 AND isstoryspotlight = 0 THEN 1 ELSE 0 END) / COUNT(id) FROM cards
