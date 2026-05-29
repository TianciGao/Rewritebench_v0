SELECT
    p.Id AS PostId,
    p.Title,
    COUNT(*) AS revision_count,
    COUNT(DISTINCT ph.UserId) AS distinct_editors,
    MIN(ph.CreationDate) AS first_revision_at,
    MAX(ph.CreationDate) AS last_revision_at,
    p.Score,
    p.ViewCount
FROM
    Posts p
JOIN
    PostHistory ph ON ph.PostId = p.Id
GROUP BY
    p.Id,
    p.Title,
    ph.UserId,
    p.Score,
    p.ViewCount
HAVING
    COUNT(*) >= 2
ORDER BY
    revision_count DESC,
    last_revision_at DESC,
    p.Id;
