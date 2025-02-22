use School
select sid,COUNT(sid) as 'count',AVG(score) as 'avg_score'
from CHOICES
group by sid