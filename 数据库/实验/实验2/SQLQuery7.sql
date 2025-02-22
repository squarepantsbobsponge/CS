use School
select sid
from CHOICES
where score>60
group by sid
having COUNT(sid)>2