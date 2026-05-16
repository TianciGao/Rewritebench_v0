WITH OutboundLinks AS (
    SELECT
        pl.PostId,
        COUNT(*) AS outbound_count
    FROM
        PostLinks pl
    GROUP BY
        pl.PostId
),
InboundLinks AS (
    SELECT
        pl.RelatedPostId AS PostId,
        COUNT(*) AS inbound_count
    FROM
        PostLinks pl
    GROUP BY
        pl.RelatedPostId
)
SELECT
    p.Id AS PostId,
    p.Title,
    COALESCE(o.outbound_count, 0) AS outbound_count,
    COALESCE(i.inbound_count, 0) AS inbound_count,
    COALESCE(o.outbound_count, 0) + COALESCE(i.inbound_count, 0) AS total_links
FROM
    Posts p
LEFT JOIN
    OutboundLinks o ON o.PostId = p.Id
LEFT JOIN
    InboundLinks i ON i.PostId = p.Id
WHERE
    COALESCE(o.outbound_count, 0) + COALESCE(i.inbound_count, 0) > 0
ORDER BY
    total_links DESC,
    p.Id;
