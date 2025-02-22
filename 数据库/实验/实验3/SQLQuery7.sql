use School
select cname
from COURSES
EXCEPT
select cname
from COURSES
where cid in(select cid
			from CHOICES)
