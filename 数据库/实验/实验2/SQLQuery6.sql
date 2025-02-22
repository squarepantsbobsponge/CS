use School
select cid,count(sid) as 'count_student'
from CHOICES
group by cid