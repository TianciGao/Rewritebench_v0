SELECT
    p.Id AS PostId,
    p.Title,
    p.Score,
    COUNT(*) AS comment_count,
    COUNT(DISTINCT c.UserId) AS distinct_commenters,
    u.DisplayName AS OwnerDisplayName
FROM
    Posts p
JOIN
    Comments c ON c.PostId = p.Id
LEFT JOIN
    Users u ON u.Id = p.OwnerUserId
WHERE
    c.UserId IS NOT NULL
GROUP BY
    p.Id,
    p.Title,
    p.Score,
    u.DisplayName,
    c.UserId
HAVING
    COUNT(*) >= 3
ORDER BY
    distinct_commenters DESC,
    p.Score DESC,
    p.Id;
