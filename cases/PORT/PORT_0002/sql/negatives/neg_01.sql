SELECT
  CAST(
    SUM(
      CASE
        WHEN `creationdate` >= '2010-01-01'
         AND `creationdate` <= '2010-12-31'
        THEN 1 ELSE 0
      END
    ) AS DOUBLE
  ) / NULLIF(
    SUM(
      CASE
        WHEN `creationdate` >= '2011-01-01'
         AND `creationdate` <= '2011-12-31'
        THEN 1 ELSE 0
      END
    ),
    0
  )
FROM `votes`;
