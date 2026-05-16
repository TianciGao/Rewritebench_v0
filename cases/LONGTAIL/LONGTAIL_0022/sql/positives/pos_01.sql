SELECT
    p.Id AS PostId,
    p.Title,
    p.Score,
    comment_stats.comment_count,
    comment_stats.distinct_commenters,
    u.DisplayName AS OwnerDisplayName
FROM
    Posts p
JOIN (
    SELECT
        c.PostId,
        COUNT(*) AS comment_count,
        COUNT(DISTINCT c.UserId) AS distinct_commenters
    FROM
        Comments c
    GROUP BY
        c.PostId
) AS comment_stats ON comment_stats.PostId = p.Id
LEFT JOIN
    Users u ON u.Id = p.OwnerUserId
WHERE
    comment_stats.comment_count >= 3
ORDER BY
    comment_stats.distinct_commenters DESC,
    p.Score DESC,
    p.Id;
