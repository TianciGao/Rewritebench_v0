SELECT
    p.Id AS PostId,
    p.Title,
    COALESCE(outbound_links.outbound_count, 0) AS outbound_count,
    COALESCE(inbound_links.inbound_count, 0) AS inbound_count,
    COALESCE(outbound_links.outbound_count, 0) + COALESCE(inbound_links.inbound_count, 0) AS total_links
FROM
    Posts p
LEFT JOIN (
    SELECT
        pl.PostId,
        COUNT(*) AS outbound_count
    FROM
        PostLinks pl
    GROUP BY
        pl.PostId
) AS outbound_links ON outbound_links.PostId = p.Id
LEFT JOIN (
    SELECT
        pl.RelatedPostId AS PostId,
        COUNT(*) AS inbound_count
    FROM
        PostLinks pl
    GROUP BY
        pl.RelatedPostId
) AS inbound_links ON inbound_links.PostId = p.Id
WHERE
    COALESCE(outbound_links.outbound_count, 0) + COALESCE(inbound_links.inbound_count, 0) > 0
ORDER BY
    total_links DESC,
    p.Id;
