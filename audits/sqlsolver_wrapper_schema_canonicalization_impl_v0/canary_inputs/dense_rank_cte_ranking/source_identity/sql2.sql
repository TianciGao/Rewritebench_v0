WITH ranked AS (SELECT id, DENSE_RANK() OVER (PARTITION BY owner_id ORDER BY score DESC) AS r FROM posts) SELECT id FROM ranked WHERE r = 1
