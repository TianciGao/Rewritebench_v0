SELECT
    ranked.UserName,
    ranked.TotalPosts,
    ranked.TotalQuestions,
    ranked.TotalAnswers,
    ranked.LastPostTitle,
    ranked.LastPostDate,
    ranked.AvgUpVotes,
    ranked.AvgDownVotes,
    ranked.Reputation,
    ranked.Views,
    ranked.rank_value
FROM (
    SELECT
        u.DisplayName AS UserName,
        COUNT(DISTINCT p.Id) AS TotalPosts,
        SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS TotalQuestions,
        SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS TotalAnswers,
        p.Title AS LastPostTitle,
        MAX(p.CreationDate) AS LastPostDate,
        AVG(COALESCE(vc.UpVotes, 0)) AS AvgUpVotes,
        AVG(COALESCE(vc.DownVotes, 0)) AS AvgDownVotes,
        u.Reputation,
        u.Views,
        ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT p.Id) DESC) AS rank_value
    FROM Users u
    LEFT JOIN Posts p ON u.Id = p.OwnerUserId
    LEFT JOIN (
        SELECT
            PostId,
            SUM(CASE WHEN VoteTypeId = 2 THEN 1 ELSE 0 END) AS UpVotes,
            SUM(CASE WHEN VoteTypeId = 3 THEN 1 ELSE 0 END) AS DownVotes
        FROM Votes
        GROUP BY PostId
    ) AS vc ON p.Id = vc.PostId
    WHERE u.Reputation > 1000
    GROUP BY u.DisplayName, p.Title, u.Reputation, u.Views
    HAVING COUNT(DISTINCT p.Id) > 0
) AS ranked
ORDER BY ranked.TotalPosts DESC, ranked.LastPostDate DESC
LIMIT 10;
