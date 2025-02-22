use School
select sname
from STUDENTS 
EXCEPT
select sname
from STUDENTS,CHOICES
where STUDENTS.sid=CHOICES.sid and CHOICES.cid=(select cid
												from COURSES
												where cname='java')