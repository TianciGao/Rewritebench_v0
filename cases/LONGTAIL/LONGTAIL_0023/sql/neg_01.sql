SELECT
    p.Id AS PostId,
    p.Title,
    COUNT(pl.RelatedPostId) AS outbound_count,
    COUNT(pl.RelatedPostId) AS inbound_count,
    COUNT(pl.RelatedPostId) * 2 AS total_links
FROM
    Posts p
LEFT JOIN
    PostLinks pl ON pl.PostId = p.Id
WHERE
    pl.RelatedPostId IS NOT NULL
GROUP BY
    p.Id,
    p.Title
HAVING
    COUNT(pl.RelatedPostId) > 0
ORDER BY
    total_links DESC,
    p.Id;
