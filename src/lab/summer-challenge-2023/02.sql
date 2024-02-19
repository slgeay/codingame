-- SQL request(s)​​​​​​‌​‌​​‌​​​​‌​​​‌‌‌​​​‌‌‌​‌ below
SELECT agent.name, count(*) as score
FROM mutant LEFT JOIN agent ON mutant.recruiterId = agent.agentId
GROUP BY mutant.recruiterId
ORDER BY score DESC
LIMIT 10;