use School
select sid,sum(score) as 'total_scores'
from CHOICES 
group by sid
having sum(score)>400
