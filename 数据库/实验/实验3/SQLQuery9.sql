use School
SELECT sid
from CHOICES,COURSES
where CHOICES.cid=COURSES.cid and COURSES.cname='database'
INTERSECT
SELECT sid
from CHOICES,COURSES
where CHOICES.cid=COURSES.cid and COURSES.cname='uml'