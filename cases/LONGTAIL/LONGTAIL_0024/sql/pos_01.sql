SELECT
    p.Id AS PostId,
    p.Title,
    history_stats.revision_count,
    history_stats.distinct_editors,
    history_stats.first_revision_at,
    history_stats.last_revision_at,
    p.Score,
    p.ViewCount
FROM
    Posts p
JOIN (
    SELECT
        ph.PostId,
        COUNT(*) AS revision_count,
        COUNT(DISTINCT ph.UserId) AS distinct_editors,
        MIN(ph.CreationDate) AS first_revision_at,
        MAX(ph.CreationDate) AS last_revision_at
    FROM
        PostHistory ph
    GROUP BY
        ph.PostId
) AS history_stats ON history_stats.PostId = p.Id
WHERE
    history_stats.revision_count >= 2
ORDER BY
    history_stats.revision_count DESC,
    history_stats.last_revision_at DESC,
    p.Id;
