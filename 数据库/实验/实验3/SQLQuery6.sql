use School
select sid,score
from CHOICES,COURSES
where CHOICES.cid=COURSES.cid and COURSES.cname='erp' and CHOICES.score IS NOT NULL and CHOICES.score>=all(select score
																			from CHOICES,COURSES
																			where CHOICES.cid=COURSES.cid and COURSES.cname='erp' and CHOICES.score IS NOT NULL)