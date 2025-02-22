use School
select STUDENTS.sid,sname
from CHOICES ,STUDENTS,COURSES
where COURSES.cname='java'AND CHOICES.cid=COURSES.cid AND CHOICES.sid=STUDENTS.sid