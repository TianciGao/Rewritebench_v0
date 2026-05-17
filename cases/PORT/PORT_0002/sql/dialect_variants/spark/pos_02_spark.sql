SELECT
  CAST(
    SUM(
      CASE
        WHEN date_format(CAST(`creationdate` AS TIMESTAMP), 'yyyy') = '2010'
        THEN 1 ELSE 0
      END
    ) AS DOUBLE
  ) / NULLIF(
    SUM(
      CASE
        WHEN date_format(CAST(`creationdate` AS TIMESTAMP), 'yyyy') = '2011'
        THEN 1 ELSE 0
      END
    ),
    0
  )
FROM `votes`;
