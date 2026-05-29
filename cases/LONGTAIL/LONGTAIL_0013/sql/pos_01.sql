SELECT
    u.DisplayName,
    COUNT(DISTINCT p.Id) AS AnsweredQuestions,
    COALESCE(AVG(p.Score), 0) AS AvgScore,
    us.TotalBounty,
    us.GoldBadges,
    us.QuestionCount,
    best_posts.Body AS BestPostContent
FROM Users u
LEFT JOIN Posts p
  ON u.Id = p.OwnerUserId
 AND p.PostTypeId = 2
LEFT JOIN (
    SELECT ranked.OwnerUserId, posts.Body
    FROM (
        SELECT
            p.Id AS PostId,
            p.OwnerUserId,
            ROW_NUMBER() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC) AS rank_value
        FROM Posts p
        WHERE p.PostTypeId = 1
    ) AS ranked
    JOIN Posts posts ON ranked.PostId = posts.Id
    WHERE ranked.rank_value = 1
) AS best_posts
  ON u.Id = best_posts.OwnerUserId
LEFT JOIN (
    SELECT
        u.Id AS UserId,
        COALESCE(SUM(v.BountyAmount), 0) AS TotalBounty,
        SUM(CASE WHEN b.Class = 1 THEN 1 ELSE 0 END) AS GoldBadges,
        COUNT(DISTINCT p.Id) AS QuestionCount
    FROM Users u
    LEFT JOIN Votes v ON u.Id = v.UserId AND v.VoteTypeId IN (8, 9)
    LEFT JOIN Badges b ON u.Id = b.UserId
    LEFT JOIN Posts p ON u.Id = p.OwnerUserId AND p.PostTypeId = 1
    GROUP BY u.Id
) AS us
  ON u.Id = us.UserId
WHERE u.Reputation > 1000
GROUP BY u.DisplayName, us.TotalBounty, us.GoldBadges, us.QuestionCount, best_posts.Body
HAVING COUNT(DISTINCT p.Id) > 0
ORDER BY AvgScore DESC, TotalBounty DESC;
