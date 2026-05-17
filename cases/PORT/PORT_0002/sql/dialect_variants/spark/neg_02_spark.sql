SELECT
  CAST(
    SUM(
      CASE
        WHEN CAST(`creationdate` AS TIMESTAMP) >= CAST('2010-01-01' AS TIMESTAMP)
         AND CAST(`creationdate` AS TIMESTAMP) <= CAST('2010-12-31' AS TIMESTAMP)
        THEN 1 ELSE 0
      END
    ) AS DOUBLE
  ) / NULLIF(
    SUM(
      CASE
        WHEN CAST(`creationdate` AS TIMESTAMP) >= CAST('2011-01-01' AS TIMESTAMP)
         AND CAST(`creationdate` AS TIMESTAMP) <= CAST('2011-12-31' AS TIMESTAMP)
        THEN 1 ELSE 0
      END
    ),
    0
  )
FROM `votes`;
