WITH CommentStats AS (
    SELECT
        c.PostId,
        COUNT(*) AS comment_count,
        COUNT(DISTINCT c.UserId) AS distinct_commenters
    FROM
        Comments c
    GROUP BY
        c.PostId
)
SELECT
    p.Id AS PostId,
    p.Title,
    p.Score,
    cs.comment_count,
    cs.distinct_commenters,
    u.DisplayName AS OwnerDisplayName
FROM
    CommentStats cs
JOIN
    Posts p ON p.Id = cs.PostId
LEFT JOIN
    Users u ON u.Id = p.OwnerUserId
WHERE
    cs.comment_count >= 3
ORDER BY
    cs.distinct_commenters DESC,
    p.Score DESC,
    p.Id;
