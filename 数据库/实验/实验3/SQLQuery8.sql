use School
SELECT distinct cname
from COURSES,CHOICES
where CHOICES.cid=COURSES.cid and CHOICES.tid in (select tid
											from COURSES ,CHOICES
											where COURSES.cid=CHOICES.cid and COURSES.cname='uml')